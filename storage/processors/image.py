# pillow 
from PIL import Image

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class ProcessImage:

    image = None

    # initilize the class
    def __init__(self,image):
        # TODO: expand the function for image path
        '''
        Initiate the image processor

        Initiate the image processor class, it takes image as the input and created the image object.

        Parameters
        ----------
        image : file
            Image file as input

        Returns
        -------
        None
            It create the image object for further uses

        Raises
        ------
        AttributeError
            If `image` is not provided.

        Examples
        --------
        >>> from storage.image_prosessor import ProcessImage
        >>> im = ProcessImage('image.jpeg')
        '''
        try:
            self.image = Image.open(image)
        except Exception as e:
            logger.error(f'ProcessImage.__init__ : {e}')

    def size(self):
        return self.image.size

    def get_average_color(self):
        image = self.image.resize((1, 1))
        color = image.getpixel((0, 0))
        return ('#{:02x}{:02x}{:02x}'.format(*color))
