from pathlib import Path
from typing import Optional

from ..crow.jupyter_notebook import nbu
from ..swan import yellow

# Import Google Colab-specific modules if running in Colab
if nbu.is_colab():
    from google.colab import output, drive, errors


class GoogleColabUtils:
    """
    A utility class for interacting with Google Colab-specific features,
    such as connecting to Google Drive and sending notifications.
    """

    @classmethod
    def mount_google_drive(cls, drive_path: str = '/content/drive') -> Optional[Path]:
        """
        Mounts Google Drive in Google Colab.

        Args:
            drive_path (str): The path where Google Drive will be mounted.
                            Default is '/content/drive'.
        Returns:
            Optional[Path]: Returns the Path where Google Drive is mounted if running in Colab,
                            otherwise returns None.
        """
        if not nbu.is_colab():
            return None

        print(yellow('Connecting to Google Drive to save model parameters and figures.'))
        cls.notification()
        drive.mount(drive_path)

        return Path(drive_path)

    @classmethod
    def notification(cls, sound: str = 'https://static.wikia.nocookie.net/soundeffects/images/c/c8/IOS_Message_Tone_Sound.ogg'):
        """
        Plays a notification sound in Google Colab.

        Args:
            sound (str): The URL of the sound to play.
                        Default is an iOS message tone sound.
        """
        if not nbu.is_colab():
            return None
        try:
            output.eval_js(f'new Audio("{sound}").play()')
        except errors.Error:
            pass


gc_utils: GoogleColabUtils = GoogleColabUtils()
gcu: GoogleColabUtils = gc_utils
