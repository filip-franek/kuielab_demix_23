import os
import numpy as np
import soundfile

from my_submission.user_config import MySeparationModel

class Inference:
    """
        Run inference on music file
    """

    def __init__(self):
        self.model = MySeparationModel()
        self.instruments = ['bass', 'drums', 'other', 'vocals']
        self.dataset_dir='./inputs/'
        self.predictions_dir='./outputs/' 
        assert os.path.exists(self.predictions_dir), f'{self.predictions_dir} - No such directory'
        assert os.path.exists(self.dataset_dir), f'{self.dataset_dir} - No such directory'

    def check_output(self, separated_music_arrays, output_sample_rates):
        assert set(self.instruments) == set(separated_music_arrays.keys()), "All instrument not present"
    
    def save_prediction(self, prediction_path, separated_music_arrays, output_sample_rates):
        if not os.path.exists(prediction_path):
            os.mkdir(prediction_path)
            
        for instrument in self.instruments:
            full_path = os.path.join(prediction_path, f'{instrument}.wav')
            soundfile.write(full_path, 
                            data=separated_music_arrays[instrument],
                            samplerate=output_sample_rates[instrument])
    
    def separate_music_file(self, filename):
        foldername = ""
        full_path = os.path.join(self.dataset_dir, foldername, filename)
        music_array, samplerate = soundfile.read(full_path)
        
        separated_music_arrays, output_sample_rates = self.model.separate_music_file(music_array, samplerate)

        self.check_output(separated_music_arrays, output_sample_rates)

        prediction_path = os.path.join(self.predictions_dir, foldername)
        self.save_prediction(prediction_path, separated_music_arrays, output_sample_rates)

        return True


if __name__ == "__main__":
    model = Inference()
    model.separate_music_file("audio_example.mp3")