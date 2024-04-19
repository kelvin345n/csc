/************************************************************************
**
** NAME:        steganography.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**				Justin Yokota - Starter Code
**				Kelvin Nguyen
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"

//Determines what color the cell at the given row/col should be. This should not affect Image, and should allocate space for a new Color.
Color *evaluateOnePixel(Image *image, int row, int col)
{
	int index = (row * image->cols) + col;
	Color* cp = image->image[index];
	uint8_t blue = cp->B;
	// Get the last bit of blue.
	uint8_t last_bit = blue & 1;

	Color* return_color = (Color*) malloc(sizeof(Color));
	if (return_color == NULL){
		// Deals with Null later
		return return_color;
	}

	// If last_bit is 0 then R is 0, but if it is 1 then R equals to 255;
	return_color->R = last_bit * 255;
	return_color->G = last_bit * 255;
	return_color->B = last_bit * 255;

	return return_color;
}

//Given an image, creates a new image extracting the LSB of the B channel.
Image *steganography(Image *image)
{
	Image* new_image = (Image*) malloc(sizeof(Image));
	if (new_image == NULL){
		printf("Mem Alloc Error");
		exit(69);
	}

	new_image->cols = image->cols;
	new_image->rows = image->rows;

	uint32_t image_length = new_image->cols*new_image->rows;

	// Array of all the pixels in the image
	new_image->image = (Color**) malloc(image_length * sizeof(Color*));
	if (new_image->image == NULL){
		free(new_image);
		printf("Mem Alloc Error");
		exit(69);
	}


	//Set each elem in image to a color
	for (int i = 0; i < image_length; i++){
		int row = i/new_image->cols;
		int col = i%new_image->rows;
		new_image->image[i] = evaluateOnePixel(image, row, col);

		if (new_image->image[i] == NULL){
			for(int j = 0; j < i; j++){
				free(new_image->image[j]);
			}
			free(new_image->image);
			free(new_image);
			printf("Mem Alloc Error");
			exit(69);
		}
	}
	return new_image;
}

/*
Loads a file of ppm P3 format from a file, and prints to stdout (e.g. with printf) a new image, 
where each pixel is black if the LSB of the B channel is 0, 
and white if the LSB of the B channel is 1.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a file of ppm P3 format (not necessarily with .ppm file extension).
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!
*/
int main(int argc, char **argv)
{	
	if (argc == 2){
		Image* original_image = readData(argv[1]); //Reads in file path to ppm P3 file and create an image
		Image* new_image = steganography(original_image);
		freeImage(original_image);
		writeData(new_image);
		freeImage(new_image);
	} else {
		printf("Invalid Arguments");
		exit(-1);
	}
	return 0;
}

