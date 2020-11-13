#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This program takes an audio file and a background image as input and visualizes
audio. Visualization is inspired by KITT (Knight Industries Two Thousand) Car
which was a character in the Knight Rider series. For more information and
examples please visit https://www.github.com/tapirlab/kitt-effect

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Tapir Lab's KITT Effect Visualization Tool for Podcasts
%% -------------------
%% $Author: Halil Said Cankurtaran$,
%% $Date: November 1st, 2020$,
%% $Revision: 1.5$
%% $Tapir Lab.$
%% $Copyright: Halil Said Cankurtaran, Tapir Lab.$
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""
import subprocess
import cv2
import numpy as np
from math import floor, ceil
from pydub import AudioSegment
from pydub.utils import make_chunks


def load_and_process_audio(audio_file_name):
    """Loads audio file and processes recording

    DC offset should be removed from audio and it should be normalized before
    mean energy calculation to get better results.

    Args:
        audio_file_name: name of the audio to process

    Returns:
        record: normalized and DC removed AudioSegment object

    Raises:
        FileNotFoundError: if audio_file_name could not loaded
    """
    try:
        record = AudioSegment.from_file(audio_file_name)
    except FileNotFoundError:
        print("Audio file could not find on the specified (%s) path!" %audio_file_name)
        raise FileNotFoundError

    # Check wheter audio is mono or not. If not then set to mono
    if record.channels != 1:
        record = record.set_channels(1)

    # Remove DC ofsett on recording and normalize to [-1, 1]
    record = record.normalize().remove_dc_offset()
    # Create chunks based on given FPS value

    return record


def rect_coords(center, width, height):
    """Returns coordinates of rectangles

    This function returns bottom-left and top-right coordinates of rectangles
    to draw on the image

    Args:
        center: Center point of the image
        width: Width of each rectangle
        height: Height of each rectangle

    Returns:
        pt1: Bottom-left of rectangle
        pr2: Top-right of rectangle
    """

    pt1 = (int(center[0]-width/2), int(center[1]-height/2))
    pt2 = (int(center[0]+width/2), int(center[1]+height/2))

    return pt1, pt2



def calculate_energy_level_of_chunks(record, FPS):
    """Calculates energy level of each cunk in specified 1/FPS seconds

    The mean energy of each chunk in the audio file should be calculated to visualize
    voice activity. However, if the calculated mean energy is directly used,
    visualization does not produce the desired output. Thus, the histogram of chunk
    energies is processed. This can be considered as a primitive histogram
    equalization technique.

    Args:
        record: Normalized and DC removed AudioSegment object
        FPS: Number of frames per second that created video has

    Returns:
        energy_of_chunks: Histogram equalized mean energy of each chunk
    """
    # Divide record into chunks
    chunks = make_chunks(record, 1000/FPS)
    # Create an empty array of length chunks to store mean energy of each
    energy_of_chunks = np.zeros(len(chunks))
    # Calculate mean energy of each chunk
    for (chunk, i) in zip(chunks, range(len(chunks))):
        tmp = np.array(chunk.get_array_of_samples().tolist(), np.float64)
        energy_of_chunks[i] = np.mean(tmp**2)

    # A pritmitive way of histogram equalization to visulize voice activity
    # First normalize, then take square root and multiply by 10
    energy_of_chunks = np.sqrt(energy_of_chunks/energy_of_chunks.max())*10

    return energy_of_chunks


def get_number_of_rectangles(energy_of_chunks, FPS):
    """Determines the representative rectangle number for each chunk based
    on calculated mean energy

    Previously calculated and equalized levels of energy for each chunk
    used to determine the number of rectangles to represent voice activity.
    An integer value between 0 and 21 returned.

    Args:
        energy_of_chunks: histogram equalized mean energy of each chunk
        FPS: frames per second - Should be given as 10 or 15

    Returns:
        levels: representative value of voice activity on each chunk
    """
    # Experementally defined energy thresholds
    # energy_thresholds = [0.1, 0.3, 0.6, 1, 1.4, 1.8, 2.2,2.6, 3, 3.5, 5, 6, 7, 10]
    if FPS == 10:
        energy_thresholds = [0.1, 0.8, 1.6, 2.4, 3.2, 4, 5, 6, 7, 8, 10]
    elif FPS == 15:
        energy_thresholds = [0.6, 1, 1.5, 2.0, 2.5, 3, 3.5, 4, 5, 7, 10]
    else:
        print("Please specify FPS as 10 or 15")
        raise ValueError

    # Calculate levels to visualize activity on chunks.
    # Create an np array to store values
    number_of_rectangles = np.zeros(len(energy_of_chunks), dtype=np.uint8)
    for (each_chunk, i) in zip(energy_of_chunks, range(len(energy_of_chunks))):
        counter, division = 0, 0
        while division != 1: # Iterate untill chunk energy matches a threshold
            if round(each_chunk / energy_thresholds[counter]) == 0:
                division = 1
            else:
                division = round(each_chunk / energy_thresholds[counter])
                counter += 1

        # Save level of chunk
        if counter == 0:
            number_of_rectangles[i] = 0
        else:
            number_of_rectangles[i] = counter*2 + 1

    return number_of_rectangles


def draw_column(img, center, count, width, height):
    """Draws each column based on the given count, width and height of rectangles

    Each column should be drawn separately. This function draws counts of
    rectangles to given img based on coordinates, width, and height
    information.

    Args:
        img: An image to draw rectangles on
        center: Center coordinates of column
        count: Number of rectangles to be drawn
        width: Width of each rectangle
        height: Height of each rectangle

    Returns:
        img: An image with rectangles drawn
    """
    # Space between each rectangle in pixels
    vspace = 5
    # Draw each rectangle
    # Color of each rectangle is set acc. to order
    red = 150
    for i in range(0, count):
        if i == 0:  # Draw center rectangle
            # Get bottom-left and top-right points of rectangle
            pt1, pt2 = rect_coords(center, width, height)
            # Draw rectangle on image, color is set to 180
            cv2.rectangle(img, pt1, pt2, (0, 0, red), -1, 8)
        if i > 0 and i < count/2:
            # Get the center of rectangle based on height and vspace
            tmp_center = (center[0], center[1]+(i*(height+vspace)))
            # Get bottom-left and top-right points of rectangle
            pt1, pt2 = rect_coords(tmp_center, width, height)
            # Draw rectangle on image, -1 means filled
            cv2.rectangle(img, pt1, pt2, (0, 0, red+(10*i)), -1, 8)
        if i > count/2:
            # Get the center of rectangle based on height and vspace
            tmp_center = (center[0], center[1]-((i-floor(count/2))*(height+vspace)))
            # Get bottom-left and top-right points of rectangle
            pt1, pt2 = rect_coords(tmp_center, width, height)
            # Draw rectangle on image, -1 means filled
            cv2.rectangle(img, pt1, pt2, (0, 0, red+(10*(ceil(i % (count/2))))), -1, 8)

    return img


def draw_rectangles(img, center_coordinate_of_column, count, width, height):
    """Draws rectangles to given image

    Each column should be drawn separately. Thus, the draw_column function is
    called to draw rectangles based on their index to set the position of the center

    Args:
        img: an image to draw rectangles on
        center_coordinate_of_column: center coordinate of column
        count: number of rectangles to be drawn
        width: width of each rectangle
        height: height of each rectangle

    Returns:
        img: an image with rectangles drawn
    """
    center = center_coordinate_of_column  # Store variable on a shorter one
    index = [-2, -1, 0, 1, 2]  # Position of column, -2 leftmost, 2 rightmost
    hspace = 40  # horizontal space between each column in px.
    # Draw each column seperately
    for i in index:
        if i == 0:
            img = draw_column(img, (center[0]+(i*hspace), center[1]), count, width, height)
        if i in (-1, 1):
            img = draw_column(img, (center[0]+(i*hspace), center[1]), count-2, width, height)
        if i in (-2, 2):
            img = draw_column(img, (center[0]+(i*hspace), center[1]), count-4, width, height)

    return img


def process_video(number_of_rectangles, background_image, video_file_name, FPS):
    """Produces a video wich audio is not included by merging each frame

    All the visualization is performed in this function. This function draws
    rectangles to each frame of video and then saves as an `.mp4` file.
    The video will be in the size of the given background image which is specified as
    1920x1080 in sample input.

    Args:
        number_of_rectangles: Number of rectangles for each chunk
        background_image: Path to background image
        video_file_name: Path to video file which only includes visualization
        FPS: Frames per second
    """
    # Load background image
    try:
        img = cv2.imread(background_image)
    except FileNotFoundError:
        print("Can't load background image!")
        raise FileNotFoundError

    img_w, img_h = img.shape[1], img.shape[0]  # Video configurations
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify extension of output
    # Create video writer object
    out = cv2.VideoWriter(video_file_name, fourcc, FPS, (img_w, img_h))

    # Configure position and dimensions of rectangles
    rect_w, rect_h = 20, 6  # Dimensions of drawn rectangles
    additional_vspace = 150  # To down shift 150px from center of image
    # (0,0) is the top-left of image.
    center_position = round(img_w/2), round(img_h/2) + additional_vspace

    for each_chunk in number_of_rectangles:
        tmp = img.copy()
        draw_rectangles(tmp, center_position, each_chunk, rect_w, rect_h)
        out.write(tmp)

    out.release()  # Save video as specified


def produce_final_output(audio_file_name, video_file_name, final_video_file):
    """Merges video with audio"""

    subprocess.call(['ffmpeg', '-i', video_file_name, '-i', audio_file_name,
                     '-shortest', '-c:v', 'copy', '-c:a', 'aac',
                     '-b:a', '128k', '-y', final_video_file])
