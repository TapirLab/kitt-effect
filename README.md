# Tapir Lab's KITT Effect Visualization Tool for Podcasts
![Tapir Lab.](http://tapirlab.com/wp-content/uploads/2020/10/tapir_logo.png)
This repository introduces a kind of audio visualization tool for Podcasts which is inspired by KITT (Knight Industries Two Thousand) which was one of the main characters of the Knight Rider series.
## Description
Podcasts can be thought of as the recordings of people's ideas, interpretations, and knowledge. By definition, it only includes audio, yet, people are encouraged to publish their works on popular platforms like YouTube. This approach requires a kind of audio-visualization of the acoustic signal to intrigue attention. This tool is built in order to provide a tool to visualize audio. 

## Prerequisites

* Python3
* ffmpeg
* Other necessary packages can be installed via `pip install -r requirements.txt`

**Note**: _requirements.txt_ includes opencv-python package. This should be noted that this package only includes fundamental functionalities of OpenCV library. Therefore, in case of need OpenCV should be installed separately.

## Folder Structure

```
KITT
|── sample_input
|   |── A short part of a podcast
|── sample_output
|   |── A short example output
|── kitt_effect.py
|── LICENSE
|── main.py
|── README.md
|── requirements.txt
```
## Example 
After installing requirements, this repo can be tested by executing the `main.py` script. It will produce an example video and save it to the `sample_output` folder. An explanation of each line of `main.py` can be found below. `FPS` parameter can only take `10` and `15` values which are defined experimentally. It can be modified to the desired value after deciding the correct energy threshold levels. Also, an example output can be seen below. This footage is taken from one of the podcasts published on the official YouTube channel of `TapirCast` who is both the developer and user of this repository. Click on the example output to access original video which includes both visualization and audio (in Turkish) together. 

[![Example Output](./sample_output/sample_output.gif)](https://youtu.be/OskxX_T42_I)



```python
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
%% $Revision: 1.6$
%% $Tapir Lab.$
%% $Copyright: Halil Said Cankurtaran, Tapir Lab.$
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
"""

import os
import kitt_effect as ke

if __name__ == "__main__":
    # Path to input audio
    audio_file_name = os.path.join(".", "sample_input", "sample_input.mp3")
    # Path to video background
    background_image = os.path.join(".", "sample_input", "bg.png")
    # Path to temporary video file which does not include audio
    video_file_name = os.path.join(".", "sample_output", "output.mp4")
    # Path to final output, which includes visualisation and audio
    final_video_file = os.path.join(".", "sample_output", "final.mp4")
    # Frames per second configuration of video
    FPS = 10
    
    # Following function loads an audio file, removes DC, and normalizes it.
    record = ke.load_and_process_audio(audio_file_name)
    # Calculate mean energy of each chunk which is partitioned based on FPS
    energy_of_chunks = ke.calculate_energy_level_of_chunks(record, FPS)
    # Determine number of rectangles to draw acc. to. mean energy level of chunk
    number_of_rectangles = ke.get_number_of_rectangles(energy_of_chunks, FPS)
    
    # Produce first video with KITT Effect
    ke.process_video(number_of_rectangles, background_image, video_file_name, FPS)
    # Merge video with audio and save to sample_output file
    ke.produce_final_output(audio_file_name, video_file_name, final_video_file)
```
## License and Citation

The software is licensed under the MIT License.
