1. Project Description

This algorithm classifies eye movements using coordinates data from a webcam. Even though this algorithm classifies eye movements, it does not work as an eye-tracking algorithm. Please refer to the URLs below if you need eye-tracking tools for your research.

1. Gazerecorder: https://gazerecorder.com/gazeflow/
2. Webgazer: https://webgazer.cs.brown.edu/

Also, the most critical point of this algorithm is that it does not provide post saccades or glissades movements, which need more elaborate techniques. This algorithm only categorizes and handles fixation, saccade, blinks, and gaps. Please refer to the URLs below if you need a more advanced eye movement classifier.

1. REMoDNaV: https://github.com/psychoinformatics-de/remodnav
2. Nyström, M., Holmqvist, K. An adaptive algorithm for fixation, saccade, and glissade detection in eyetracking data. Behavior Research Methods 42, 188–204 (2010). https://doi.org/10.3758/BRM.42.1.188

I develop this algorithm to tailor the data pipeline for a specific purpose, only for handling fixations properly. 

Reference

1. Olsen, A. (2012, March). The Tobii I-VT Fixation Filter: Algorithm description. tobii.
2. Salvucci, D. D., & Goldberg, J. H. (2000, November). Identifying fixations and saccades in eye-tracking protocols. In Proceedings of the 2000 symposium on Eye tracking research & applications (pp. 71-78).
3. Dar, A.H., Wagner, A.S. & Hanke, M. REMoDNaV: robust eye-movement classification for dynamic stimulation. Behav Res 53, 399–414 (2021). https://doi.org/10.3758/s13428-020-01428-x