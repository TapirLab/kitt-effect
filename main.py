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

import os
import kitt_effect as ke

if __name__ == "__main__":
    # Path to input audio
    AUDIO_FILE_NAME = os.path.join(".", "sample_input", "sample_input.mp3")
    # Path to video background
    BACKGROUND_IMAGE = os.path.join(".", "sample_input", "bg.png")
    # Path to temporary video file which does not include audio
    VIDEO_FILE_NAME = os.path.join(".", "sample_output", "output.mp4")
    # Path to final output, which includes visualisation and audio
    FINAL_VIDEO_FILE = os.path.join(".", "sample_output", "final.mp4")
    # Frames per second configuration of video
    FPS = 10

    # Following function loads an audio file, removes DC, and normalizes it.
    RECORD = ke.load_and_process_audio(AUDIO_FILE_NAME)
    # Calculate mean energy of each chunk which is partitioned based on FPS
    ENERGY_OF_CHUNKS = ke.calculate_energy_level_of_chunks(RECORD, FPS)
    # Determine number of rectangles to draw acc. to. mean energy level of chunk
    NUMBER_OF_RECTANGLES = ke.get_number_of_rectangles(ENERGY_OF_CHUNKS, FPS)

    # Produce first video with KITT Effect
    ke.process_video(NUMBER_OF_RECTANGLES, BACKGROUND_IMAGE, VIDEO_FILE_NAME, FPS)
    # Merge video with audio and save to sample_output file
    ke.produce_final_output(AUDIO_FILE_NAME, VIDEO_FILE_NAME, FINAL_VIDEO_FILE)
