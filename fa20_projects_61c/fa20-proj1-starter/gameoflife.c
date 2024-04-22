/************************************************************************
**
** NAME:        gameoflife.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Justin Yokota - Starter Code
**				YOUR NAME HERE
**
**
** DATE:        2020-08-23
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include "imageloader.h"


uint32_t calculateIndex(int row, int col, Image *image){
	row = (row + image->rows) % image->rows;
	col = (col + image->cols) % image->cols; 
	return ((row * image->cols) + col);
}
// Calculates the 24 bit pattern where the first 8 bits are nothing burgers.
// (Last 24 bits contains the color information, where second 8 bits contains red
// next 8 contains green, and last 8 contains blue). 
uint32_t calculateColorBitPattern(Color* color){
	uint32_t color_bit_pattern = 0;

	color_bit_pattern += ((uint32_t)color->R << 16);
	color_bit_pattern += ((uint32_t)color->G << 8);
	color_bit_pattern += ((uint32_t)color->B);

	return color_bit_pattern;
}

// Returns 1 if alive and 0 if dead. 
uint32_t determineLifeness(Image* image, int row, int col, uint32_t compare_pattern){
	// Get specific color at the row and column.
	Color* color = image->image[(int)calculateIndex(row, col, image)];
	uint32_t color_pattern = calculateColorBitPattern(color);
	if (color_pattern & compare_pattern){
		return 1;
	}
	return 0;
}


// Returns the new 32 bit pattern of the color when used against the rule. 
uint32_t playGameOnBitPattern(Image* image, int row, int col, 
							uint32_t rule, uint32_t color_pattern){

	uint32_t new_bit_pattern = 0;

	for (uint32_t i = 0; i < 24; i++){
		uint32_t compare_bits = 1 << i;
		uint32_t live_neighbors = 0;
		//top-left
		live_neighbors += determineLifeness(image, row-1, col-1, compare_bits);
		// top
		live_neighbors += determineLifeness(image, row-1, col, compare_bits);
		// top-right
		live_neighbors += determineLifeness(image, row-1, col+1, compare_bits);
		// left
		live_neighbors += determineLifeness(image, row, col-1, compare_bits);
		// right
		live_neighbors += determineLifeness(image, row, col+1, compare_bits);
		// bottom-left
		live_neighbors += determineLifeness(image, row+1, col-1, compare_bits);
		// bottom
		live_neighbors += determineLifeness(image, row+1, col, compare_bits);
		// bottom-right
		live_neighbors += determineLifeness(image, row+1, col+1, compare_bits);

		uint32_t movement = live_neighbors;
		if (color_pattern & compare_bits){
			//Cell is alive at the specific bit
			movement = 9 + live_neighbors;
		}
		uint32_t rule_bits = 1 << movement;
		uint32_t next_state = rule & rule_bits;

		if (next_state){
			new_bit_pattern += compare_bits; 
		}
	}

	return new_bit_pattern;
}

//Determines what color the cell at the given row/col should be. This function allocates space for a new Color.
//Note that you will need to read the eight neighbors of the cell in question. The grid "wraps", so we treat the top row as adjacent to the bottom row
//and the left column as adjacent to the right column.
Color *evaluateOneCell(Image *image, int row, int col, uint32_t rule)
{
	// Get color
	Color* color = image->image[(int)calculateIndex(row, col, image)];
	Color* new_color = (Color*) malloc(sizeof(Color));
	if (new_color == NULL){
		return new_color;
	}

	uint32_t color_bit_pattern = calculateColorBitPattern(color);
	color_bit_pattern = playGameOnBitPattern(image, row, col, rule, color_bit_pattern);

	new_color->B = color_bit_pattern & 255; // Extracts the 8 bit pattern
	color_bit_pattern >>= 8; 
	new_color->G = color_bit_pattern & 255;
	color_bit_pattern >>= 8;
	new_color->R = color_bit_pattern;

	return new_color;
}

//The main body of Life; given an image and a rule, computes one iteration of the Game of Life.
//You should be able to copy most of this from steganography.c
Image *life(Image *image, uint32_t rule)
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
		int col = i%new_image->cols;
		new_image->image[i] = evaluateOneCell(image, row, col, rule);

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
Loads a .ppm from a file, computes the next iteration of the game of life, then prints to stdout the new image.

argc stores the number of arguments.
argv stores a list of arguments. Here is the expected input:
argv[0] will store the name of the program (this happens automatically).
argv[1] should contain a filename, containing a .ppm.
argv[2] should contain a hexadecimal number (such as 0x1808). Note that this will be a string.
You may find the function strtol useful for this conversion.
If the input is not correct, a malloc fails, or any other error occurs, you should exit with code -1.
Otherwise, you should return from main with code 0.
Make sure to free all memory before returning!

You may find it useful to copy the code from steganography.c, to start.
*/
int main(int argc, char **argv)
{
	Image* original_image = readData(argv[1]); //Reads in file path to ppm P3 file and create an image
	char* endptr;
	Image* new_image = life(original_image, strtol(argv[2], &endptr, 16));
	freeImage(original_image);
	
	writeData(new_image);
	freeImage(new_image);
}
// if (argc != 2){
// 		printf("usage: %s filename rule\n", argv[0]);
// 		printf("filename is an ASCII PPM file (type P3) with maximum value 255.\n");
// 		printf("rule is a hex number beginning with 0x; Life is %s.", argv[2]);
// 	} else {
// 		Image* original_image = readData(argv[1]); //Reads in file path to ppm P3 file and create an image
// 		char* endptr;
// 		Image* new_image = life(original_image, strtol(argv[2], &endptr, 16));
// 		freeImage(original_image);
		
// 		writeData(new_image);
// 		freeImage(new_image);
// 	}