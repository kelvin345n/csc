/************************************************************************
**
** NAME:        imageloader.c
**
** DESCRIPTION: CS61C Fall 2020 Project 1
**
** AUTHOR:      Dan Garcia  -  University of California at Berkeley
**              Copyright (C) Dan Garcia, 2020. All rights reserved.
**              Justin Yokota - Starter Code
**				Kelvin Nguyen - Finisher
**
**
** DATE:        2020-08-15
**
**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <inttypes.h>
#include <string.h>
#include "imageloader.h"

//Opens a .ppm P3 image file, and constructs an Image object. 
//You may find the function fscanf useful.
//Make sure that you close the file with fclose before returning.
Image *readData(char *filename) 
{
	Image* ip = (Image*) malloc(sizeof(Image));
	if (ip == NULL){
		printf("Mem Alloc Unsuccessful for Image");
		exit(69);
	}

	FILE *fp = fopen(filename, "r");
	if (fp == NULL){
		free(ip);
		printf("Unable to Open %s", filename);
		exit(69);
	}

	// Reads in the header of the image file. Not relevant
	fscanf(fp, "%*s");
	// Assigns how many rows and cols wide the image is
	fscanf(fp, "%u %u", &(ip->cols), &(ip->rows));
	// Reads in the color range. Irrelevant, assuming 0-255. 
	fscanf(fp, "%*d");
	// Allocates mem for the image array of pixels
	ip->image = (Color**) malloc((ip->rows * ip->cols)*sizeof(Color*));
	if (ip->image == NULL){
		free(ip);
		printf("Mem Alloc Unsuccessful for Image");
		fclose(fp);
		exit(69);
	}

	// Iterate over all the pixels inside of the image.
	// And assigning each pixel to the image pointer (ip).
	for (int i = 0; i < (ip->rows * ip->cols); i++){
		Color* pixel = (Color*) malloc(sizeof(Color));

		if (pixel == NULL){
			for (int j = 0; j < i; j++){
				free(ip->image[j]);
			}	
			free(ip->image);
			free(ip);
			printf("Mem Alloc Unsuccessful for Pixel");
			fclose(fp);
			exit(69);
		}
		//Assigns the RGB values to that newly created pixel
		fscanf(fp, "%hhu %hhu %hhu",&(pixel->R), &(pixel->G), &(pixel->B));

		ip->image[i] = pixel;
	}
	fclose(fp);
	return ip;
}



//Given an image, prints to stdout (e.g. with printf) a .ppm P3 file with the image's data.
void writeData(Image *image)
{
	printf("P3\n");
	printf("%u %u\n", image->cols, image->rows);
	printf("%u\n", 255);

	int counter = 0;
	
	for (int i = 0; i < image->rows; i++){
		for (int j = 0; j < image->cols; j++){
			Color* cArray = image->image[counter];
			printf("%3hhu %3hhu %3hhu   ", cArray->R, cArray->G, cArray->B);
			counter++;
		}
		printf("\n");
	}
}

//Frees an image entirely
void freeImage(Image *image)
{
	if (image != NULL){
		for (int i = 0; i < (image->cols*image->rows); i++){
			free(image->image[i]);
		}	
		free(image->image);
		free(image);
	}
}