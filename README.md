# YouTube Transcription and Analysis Tool

This tool allows users to transcribe and analyze content from YouTube videos, local video files, or directly input text. It uses speech recognition to transcribe audio and leverages OpenAI's GPT model to provide analysis and feedback on the content.

## Features

- Download and extract audio from YouTube videos
- Transcribe audio from YouTube videos or local video files
- Analyze text content using OpenAI's GPT model
- Provide feedback and scoring on essay structure, content, and language use

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- OpenAI API key
- Required Python libraries (see `requirements.txt`)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/youtube-transcription-analysis.git
   ```

2. Navigate to the project directory:
   ```
   cd youtube-transcription-analysis
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `config.py` file in the root directory and add your OpenAI API key:
   ```python
   OPEN_AI_API_KEY = 'your-api-key-here'
   ```

## Usage

Run the main script:

```
python main.py
```

Follow the prompts to choose your input method:

1. YouTube video URL
2. Local video file
3. Direct text input

The tool will then process your input and provide an analysis of the content.

## Contributing

Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

If you have any questions or feedback, please open an issue in this repository.