<div align="center">
  <h1>🎙️ OpenAI Real-Time Audio-to-Audio</h1>
  
  <p>
    <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge" alt="Python">
    <img src="https://img.shields.io/badge/Model-GPT--4o--Audio-green?style=for-the-badge" alt="GPT-4o">
    <img src="https://img.shields.io/badge/API-OpenAI-orange?style=for-the-badge&logo=openai" alt="OpenAI">
  </p>

  <p><i>A terminal interface for native voice-to-voice communication.</i></p>
</div>

## 📖 Overview
This project implements the **GPT-4o Audio Preview** model to create a low-latency voice assistant. 
Unlike traditional STT/TTS chains, this script communicates using raw audio bytes, preserving emotional inflection and reducing processing time.

## 🛠️ System Requirements

Before running the script, ensure you have **PortAudio** installed on your machine:

<table>
  <tr>
    <th>Platform</th>
    <th>Installation Command</th>
  </tr>
  <tr>
    <td><b>macOS</b></td>
    <td><code>brew install portaudio</code></td>
  </tr>
  <tr>
    <td><b>Linux</b></td>
    <td><code>sudo apt-get install python3-pyaudio</code></td>
  </tr>
  <tr>
    <td><b>Windows</b></td>
    <td>Install <a href="https://visualstudio.microsoft.com/visual-cpp-build-tools/">C++ Build Tools</a></td>
  </tr>
</table>

## 🚀 Quick Start

### 1. Installation
```bash
pip install pyaudio python-dotenv openai
```
### 2. Configuration
Create a .env file and place your **OpenAI API key**:
```bash
OPENAI_API_KEY=your_api_key_here
```
Next, create a custom **system_prompt.txt** in the root directory for your personal assistant:
```bash
Act as my mother and say that you're proud of me...
```
