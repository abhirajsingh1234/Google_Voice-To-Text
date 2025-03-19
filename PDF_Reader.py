import speech_recognition as sr
import pyttsx3
import threading
import time

# Global variables for control
is_paused = False
current_position = 0
running = True

# Break text into smaller chunks
def chunk_text(text, chunk_size=50):
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(' '.join(current_chunk)) >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks

# Function to listen for commands continuously
def command_listener():
    global is_paused, current_position, running
    
    # Initialize recognizer
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening for commands ('stop' or 'start')...")
        recognizer.adjust_for_ambient_noise(source)
        
        while running:
            try:
                command = input("enter command: ")
                
                if command == "stop" and not is_paused:
                    print("Stop command detected!")
                    is_paused = True
                    print("Speech paused. Say 'start' to resume.")
                    
                elif command == "start" and is_paused:
                    print("Start command detected!")
                    is_paused = False
                    print(f"Resuming from position {current_position}")

                elif command=="restart" and is_paused:
                    print("restart command detected!")
                    current_position = 0
                    is_paused = False
                    print("restarting the lesson")
                    
            except sr.UnknownValueError:
                pass  # No speech detected
            except sr.RequestError:
                print("Could not request results from speech recognition service")
            except Exception as e:
                print(f"Error in command listener: {str(e)}")

# Main text to speak
text = """I
        A MESSAGE FROM THE AUTHOR
        n writing Mindset Secrets for Winning, I drew upon many aspects of my life, from business
        to sports, struggles to triumphs, and rags to riches. I researched broadly, from the
        preparation of Olympic athletes to the techniques of the world's best coaches, as well as to
        every influential aspect in the lives of the successful elite. As a peak performance book,
        Mindset Secrets for Winning often emphasizes examples from sports, but it is certainly not
        limited to athletics. Those who want to become the best version of themselves in whatever
        they do will benefit from this book. I encourage all readers to keep an open mind to gather
        insights that apply to their own lives. It's important to read the entire book, as each section
        builds on the previous section. In all your pursuits, I wish you the best."""

# Clean up text formatting
text = ' '.join(line.strip() for line in text.split('\n'))

# Break text into manageable chunks
chunks = chunk_text(text)

print("Voice assistant activated. Say 'stop' to pause and 'start' to resume.")

# Start the command listener in a separate thread
listener_thread = threading.Thread(target=command_listener)
listener_thread.daemon = True
listener_thread.start()

try:
    # Main speech loop
    while current_position < len(chunks) and running:
        if not is_paused:
            chunk = chunks[current_position]
            print(f"Speaking chunk {current_position + 1}/{len(chunks)}")
            
            # Create a new engine instance for each chunk to avoid run loop issues
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.say(chunk)
            engine.runAndWait()
            engine.stop()
            
            # Move to next chunk
            current_position += 1
            
            # Small delay to give time for command processing
            time.sleep(0.1)
        else:
            # If paused, just wait a bit before checking again
            time.sleep(0.5)
    
    print("Speech completed.")
    
except KeyboardInterrupt:
    print("\nProgram interrupted by user.")
    running = False

# Clean up
running = False
if listener_thread.is_alive():
    listener_thread.join(timeout=1)

print("Program terminated.")