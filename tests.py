"""
QTconverter unit tests.
"""
import unittest
import os
import qt_files_converter

TEST_DIRECTORY = 'test_data'
TEMPLATE_CONTENT = (
    'video region="videoregion" src="{file_name}.mov" region="video"'
)


class QTFilesConverterTestCase(unittest.TestCase):

    def setUp(self):
        """
        Sets up environment before each test.
        """
        self.qt_file_name = 'Job_123_test_file.mp4_test'
        self.qt_file_content = (
            '[00:00:18.788]\n'
            '[BLANK_AUDIO]\n\n'
            '[00:00:22.399]\n\n'
            '[00:00:22.399]\n'
            '>> but our next [MUSIC] guest, our very, very\n'
            'special guest, Jeri Ellsworth, has just\n\n'
            '[00:00:28.249]\n'
        )
        self.template_smil_file_path = (
            os.path.join(TEST_DIRECTORY, 'template.smil')
        )
        self.qt_file_path = os.path.join(
            TEST_DIRECTORY, '{}{}'.format(self.qt_file_name, '.qt')
        )

        if not os.path.exists(TEST_DIRECTORY):
            os.makedirs(TEST_DIRECTORY)

        with open(self.template_smil_file_path, 'w') as template:
            template.write(TEMPLATE_CONTENT)

        with open(self.qt_file_path, 'w') as qt_file:
            qt_file.write(self.qt_file_content)

    def tearDown(self):
        """
        Get rid of unused objects after each test.
        """
        self.directory = os.path.join(os.getcwd(), 'test_data/')
        for file in os.listdir(self.directory):
            os.remove(self.directory + file)

    def test_converter(self):
        """
        Tests results after files conversion.
        """
        self.caption_file_name = '123_test_file'
        self.smil_file_path = os.path.join(
            TEST_DIRECTORY, '{}{}'.format(self.caption_file_name, '.smil')
        )
        self.qt_file_path = os.path.join(
            TEST_DIRECTORY, '{}{}'.format(self.caption_file_name, '.qt.text')
        )

        qt_files_converter.converter(TEST_DIRECTORY)

        self.assertTrue(os.path.isfile(self.qt_file_path))
        self.assertTrue(os.path.isfile(self.smil_file_path))

        with open(self.qt_file_path, 'r') as qt_file:
            result = qt_file.read()
        self.assertEqual(
            (
                '[00:00:18.788]\n\n\n\n'
                '[00:00:22.399]\n'
                '>> but our next (MUSIC) guest, our very, very\n'
                'special guest, Jeri Ellsworth, has just\n\n'
            ),
            result
        )

        with open(self.smil_file_path, 'r') as smil_file:
            result = smil_file.read()
        self.assertEqual(
            (
                'video region="videoregion" src="%s.mov" region="video"'
                % self.caption_file_name
            ),
            result
        )

    def test_get_smil_template(self):
        """
        Tests getting content of template.smil files
        """
        self.assertTrue(
            TEMPLATE_CONTENT in (
                qt_files_converter.get_smil_template(TEST_DIRECTORY)
            )
        )

if __name__ == '__main__':
    unittest.main()
