"""
Digital Detox Assistant: Your friendly neighborhood screen-time therapist 🧘‍♂️
Author: Your mindful coding companion
Version: 2.0 (Now with extra zen!)

This assistant helps users maintain a healthy relationship with technology 
through mindful reminders, activity suggestions, and a dash of digital wisdom.
Think of it as your personal Cal Newport with a sense of humor!
"""
import requests
import schedule
import time
import random
import threading
from datetime import datetime
from PIL import Image
import io
from flask import Flask, render_template, request, jsonify
import spotipy # Added import
import openai # Added import
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Deployed successfully on Render!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # 👈 this is required!
    app.run(host='0.0.0.0', port=port)         # 👈 this too!

class DigitalDetoxAssistant:
    """
    A wise (and slightly witty) digital wellness companion that helps users
    maintain healthy screen time habits while keeping their sanity intact.
    """

    def __init__(self):
        # Core attributes (or as we like to call them, "digital vital signs")
        self.screen_time_goal = None  # The user's ambitious screen time target
        self.reminder_interval = None  # How often we'll gently nudge (not nag!)
        self.running = True  # Like a meditation timer, but for your whole digital life
        self.interaction_count = 0  # Counting conversations (cheaper than therapy!)
        self.last_mood = "neutral"  # Because even chatbots have feelings
        self.user_name = None  # Your digital identity (minus the @ symbol)
        self.activity_history = []  # The chronicles of your digital detox journey

        # Deep work wisdom (carefully curated brain food)
        self.tips = [
            "Schedule specific times for deep work - your brain will thank you later!",
            "Create a dedicated workspace free from digital distractions (yes, that means hiding your phone)",
            "Practice 'analog leisure' - remember those things called books?",
            "Use technology with intention, not like a squirrel chasing notifications",
            "Implement a daily digital sunset - let your brain know it's bedtime",
            "Focus on one task at a time - your brain isn't a browser with multiple tabs",
            "Schedule email checks - inbox zero isn't a life goal",
            "Keep your phone in another room during deep work (it'll survive without you)"
        ]

        # Deep work activities (a.k.a. "Screen-Free Fun")
        self.deep_work_suggestions = [
            "Find your focus fortress: 90 minutes of uninterrupted genius time",
            "Embrace the ancient art of pen and paper (no, they're not obsolete)",
            "Take a nature walk - where notifications are just birds chirping",
            "Read a physical book (warning: may cause actual page-turning)",
            "Think without digital crutches - like our ancestors did!",
            "Have a real conversation (yes, with actual humans)",
            "Practice a hobby that doesn't need charging",
            "Organize your physical workspace (Marie Kondo would be proud)"
        ]

        # Contextual responses (wisdom for every digital dilemma)
        self.responses = {
            "social_media": [
                "Plot twist: Real life has better resolution than Instagram",
                "Breaking news: Your best life isn't waiting in your feed",
                "Consider this: Friends in real life don't need filters"
            ],
            "focus": [
                "Your focus is your superpower (no cape required)",
                "Time-blocking: Like Tetris for your productivity",
                "Deep work: Where the magic happens (and notifications don't)"
            ],
            "productivity": [
                "Productivity isn't about tools, it's about intentions (mind blown)",
                "Simple tools, remarkable results - like a pencil, but for your life",
                "Less apps, more naps - the secret to true productivity"
            ]
        }

    def read_and_focus_image(self, image_path: str) -> str:
        """
        Read an image and provide focus-related insights.
        """
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                brightness = 0
                pixels = 0

                # Convert to grayscale for brightness analysis
                gray_img = img.convert('L')
                for pixel in gray_img.getdata():
                    brightness += pixel
                    pixels += 1

                avg_brightness = brightness / pixels if pixels > 0 else 0

                # Generate focus recommendations based on image properties
                recommendations = []
                if avg_brightness < 128:
                    recommendations.append("🔆 Image appears dark - consider better lighting for reduced eye strain")
                if width < 800 or height < 600:
                    recommendations.append("📏 Image resolution is low - viewing smaller images may require more focus")

                return "\n".join([
                    "📸 Image Analysis for Focus:",
                    f"• Size: {width}x{height}",
                    f"• Average Brightness: {avg_brightness:.1f}/255",
                    "\n🎯 Focus Recommendations:",
                    *recommendations,
                    "\n💡 Tip: Take a 20-second break every 20 minutes when viewing images"
                ])
        except Exception as e:
            return f"⚠️ Could not process image: {str(e)}"

    def get_time_appropriate_activity(self) -> str:
        """
        Suggests activities based on the time of day, because timing is everything!
        Returns a mindful activity suggestion that matches the current hour.
        """
        hour = datetime.now().hour

        if 5 <= hour < 12:  # Morning wisdom
            morning_activities = [
                "Start your day with focused work (before the world wakes up)",
                "Morning meditation (because your mind needs breakfast too)",
                "Plan your deep work sessions (while your caffeine kicks in)",
                "Review goals (no screens needed, just clarity)"
            ]
            return random.choice(morning_activities)
        elif 12 <= hour < 17:  # Afternoon enlightenment
            afternoon_activities = [
                "Take a mindful walk (yes, leave the phone behind)",
                "Deep work power hour (your afternoon coffee's best friend)",
                "Strategic screen break (your eyes will write you a thank-you note)",
                "Real human interaction time (remember those?)"
            ]
            return random.choice(afternoon_activities)
        else:  # Evening zen
            evening_activities = [
                "Journal your wins (old school paper style)",
                "Read a real book (swipe-free entertainment)",
                "Non-digital hobby time (unleash your inner artist)",
                "Plan tomorrow's success (while today's still fresh)"
            ]
            return random.choice(evening_activities)

    def __init__(self):
        # Existing initialization code...
        self.api_keys = {
            'spotify': os.getenv('SPOTIFY_API_KEY', ''),
            'fitbit': os.getenv('FITBIT_API_KEY', ''),
            'openai': os.getenv('OPENAI_API_KEY', ''),
        }


    def get_music_recommendation(self) -> str:
        """Get personalized music recommendations from Spotify"""
        try:
            if self.api_keys['spotify']:
                sp = spotipy.Spotify(auth=self.api_keys['spotify'])
                playlists = sp.user_playlists('spotify')
                return "🎵 Recommended Playlist: Lo-fi Focus Beats"
            return "🎵 Default Recommendation: Try ambient music or nature sounds"
        except Exception:
            return "🎵 Explore calming instrumental music"

    def get_workout_suggestion(self) -> str:
        """Get personalized workout suggestions from Fitbit"""
        try:
            if self.api_keys['fitbit']:
                # Fitbit integration would go here
                return "💪 Suggested Activity: 10-minute cardio"
            return "💪 Default Exercise: Basic stretching routine"
        except Exception:
            return "💪 Try basic stretching exercises"

    def get_creative_prompt(self) -> str:
        """Get creative writing prompt from OpenAI"""
        try:
            if self.api_keys['openai']:
                client = openai.OpenAI(api_key=self.api_keys['openai'])
                response = client.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt="Generate a creative writing prompt",
                    max_tokens=50
                )
                return f"🎨 Prompt: {response.choices[0].text.strip()}"
            return "🎨 Default Prompt: Draw your favorite memory"
        except Exception:
            return "🎨 Express yourself through simple sketching"

    def get_activity_suggestion(self, category: str) -> str:
        """
        Returns a detailed activity suggestion based on category.
        Includes benefits, instructions, and motivation.
        """
        suggestions = {
            'a': {  # Music & Rhythm
                'activities': [
                    {
                        'title': "API-Powered Music Meditation",
                        'description': f"""🎵 {self.get_music_recommendation()}

Transform your mood with focused music listening! Find a comfortable spot, and just listen. No multitasking, no scrolling - just you and the music.

Benefits: Reduces stress, improves focus, resets your mental state
Getting Started: Pick ONE album (recommended: Lo-fi beats or Mozart)
Tip: Use physical media like vinyl or CD to avoid digital distractions
Time Needed: 30 minutes

Remember: Music isn't background noise - it's a journey for your mind! Ready to press play?"""
                    }
                ]
            },
            'b': {  # Physical Activity
                'activities': [
                    {
                        'title': "Smart Movement Break",
                        'description': f"""💪 {self.get_workout_suggestion()}

Time for a body and brain refresh! Let's do a simple but effective movement sequence that requires zero equipment and zero screentime.

The Flow:
1. 10 slow, mindful stretches
2. 20 jumping jacks
3. 1-minute quiet standing meditation

Benefits: Boosts energy, improves focus, reduces screen fatigue
Getting Started: Just stand up - that's step one!
Obstacle Buster: "No time?" These 5 minutes will make the next hour more productive!

Your body was designed to move, not scroll. Shall we begin?"""
                    }
                ]
            },
            'c': {  # Creative Expression
                'activities': [
                    {
                        'title': "AI-Inspired Creative Session",
                        'description': f"""🎨 {self.get_creative_prompt()}

Grab a paper and pencil - we're going analog! No judgment, no perfection needed - just pure creative flow.

Why This Works:
- Exercises different brain regions than digital work
- Improves hand-eye coordination
- Creates a mindful break from screens

Pro Tip: Don't erase! Embrace the beautiful imperfections.
Time Investment: Just 5 minutes

Remember: This isn't about art - it's about being present and playful!"""
                    }
                ]
            },
            'd': {  # Reading
                'activities': [
                    {
                        'title': "Digital Minimalism by Cal Newport",
                        'description': """📚 Today's Reading Adventure: "Digital Minimalism" by Cal Newport - a perfect guide for your journey towards intentional technology use.

Key Themes:
- Choosing attention over distraction
- Building meaningful offline activities
- Creating rules for digital engagement

Start With: Chapter 1, just 20 minutes
Reading Spot: Find a cozy, screen-free corner
Mindset: This isn't just reading - it's investing in your digital wellness!

Ready to dive into some life-changing wisdom?"""
                    }
                ]
            },
            'e': {  # Social Connection
                'activities': [
                    {
                        'title': "The Letter Writing Revival",
                        'description': """✉️ Let's bring back the lost art of letter writing! Choose one person you usually text with and write them a physical letter instead.

Materials Needed:
- Paper (any kind!)
- Pen
- Envelope (optional - even folded paper works!)

Why It's Special:
- Creates a unique, tangible connection
- Forces slow, thoughtful communication
- Gives both writer and recipient a screen-free moment

Challenge: Write about something you'd never text about.
Time Needed: 15-20 minutes

Ready to make someone's day in an unexpectedly analog way?"""
                    }
                ]
            }
        }

        if category in suggestions:
            activity = random.choice(suggestions[category]['activities'])
            self.activity_history.append(activity['title'])
            return f"\n🌟 {activity['title']}\n\n{activity['description']}"
        return "Category not found. Please try again."

    def send_reminder(self) -> None:
        """
        Sends mindful reminders - like a gentle tap on the shoulder from
        your digital wellness coach.
        """
        if self.running:
            current_hour = datetime.now().hour
            if 22 <= current_hour or current_hour < 6:
                print(f"\n🌙 {self.user_name}, time for digital sunset. Your brain's night mode thanks you!")
            else:
                print(f"\n⏰ {self.user_name}, mindful moment alert!")
                print("💭 Wisdom drop:", random.choice(self.tips))

    def start_reminders(self) -> None:
        """
        Keeps the reminder schedule running - like a mindfulness metronome.
        """
        schedule.every(self.reminder_interval).minutes.do(self.send_reminder)
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def show_menu(self, menu_type="main", category=None) -> str:
        """
        Displays menus based on type (main/sub) and category.
        Returns a formatted menu string.
        """
        if menu_type == "main":
            return """
            📋 Digital Wellness Menu:
            1️⃣ Focus Tips & Techniques
            2️⃣ Screen-Free Activity Suggestions
            3️⃣ Check Screen Time Goal
            4️⃣ Productivity Enhancement
            5️⃣ Social Media Reality Check
            6️⃣ Digital Wellness Report
            7️⃣ Image Focus Analysis
            8️⃣ Exit Program

            Enter a number (1-7) to choose your path to digital wellness! 🌟
            """
        elif menu_type == "activities":
            return """
            🎯 Screen-Free Activities:
            a) 🎵 Music & Rhythm - Connect with melodies and rhythms
            b) 💪 Physical Activity - Get moving and energized
            c) 🎨 Creative Expression - Unleash your artistic side
            d) 📚 Reading Adventure - Dive into a good book
            e) 🤝 Social Connection - Connect offline
            r) Return to main menu

            Choose your adventure (a-e, or r): """
        elif menu_type == "productivity":
            return """
            ⚡ Productivity Enhancement:
            a) ⏲️ Pomodoro Technique - Work in focused sprints
            b) 🧠 Deep Work Rituals - Design your focus fortress
            c) 📦 Task Batching - Group similar tasks
            d) 📅 Calendar Blocking - Time architecture
            e) 🎯 Distraction Audit - Track focus destroyers
            r) Return to main menu

            Choose your technique (a-e, or r): """

    def get_focus_tip(self) -> str:
        """Provides a detailed focus tip with implementation guidance."""
        tip = random.choice(self.tips)
        explanation = {
            "Schedule specific times": "→ Implementation: Block your calendar for 2-3 deep work sessions (90 mins each)\n→ Pro tip: Start with your most challenging task during peak energy hours",
            "Create a dedicated workspace": "→ Implementation: Choose a quiet corner, remove visible devices\n→ Pro tip: Use a simple timer instead of your phone's timer",
            "Practice 'analog leisure'": "→ Implementation: Set aside 30 minutes for reading or journaling\n→ Pro tip: Keep a book and notebook within arm's reach",
            "Use technology with intention": "→ Implementation: Write down your purpose before opening any app\n→ Pro tip: Use app timers to enforce boundaries",
            "Implement a daily digital sunset": "→ Implementation: Stop screen use 1 hour before bed\n→ Pro tip: Switch to reading or light stretching",
        }.get(tip[:25], "→ Implementation: Start with 25 minutes of focused work\n→ Pro tip: Take a 5-minute break between sessions")

        return f"\n🎯 Focus Wisdom:\n{tip}\n\n{explanation}"

    def get_productivity_technique(self, technique: str) -> str:
        """Returns detailed explanation of productivity techniques."""
        techniques = {
            'a': """⏲️ Pomodoro Technique - Your Focus Sprint Guide:
            Step 1: Set a timer for 25 minutes
            Step 2: Focus on one task until the timer rings
            Step 3: Take a 5-minute break
            Step 4: After 4 sessions, take a longer 15-30 minute break

            Pro Tip: It's like giving your brain a workout with built-in rest periods!
            Challenge: Complete 4 Pomodoros today without checking social media.""",

            'b': """🧠 Deep Work Rituals - Build Your Focus Fortress:
            1. Choose your quiet space (a room, corner, or desk)
            2. Set a 90-minute deep work window
            3. Shut off ALL notifications
            4. Put up a "Do Not Disturb" sign
            5. Keep only essential tools visible

            Key Point: Deep work is like weightlifting for your concentration muscles!
            Start Small: Begin with 45 minutes and work your way up.""",

            'c': """📦 Task Batching - Group Similar Tasks:
            • Email Time: Check all emails in one 30-minute block
            • Call Time: Schedule all calls back-to-back
            • Creative Time: Group all writing/design tasks
            • Admin Time: Handle paperwork in one session

            Why It Works: Your brain stays in one mode, saving mental energy!
            Try This: Batch all your meetings into "Meeting Mondays" or "Talk Tuesdays".""",

            'd': """📅 Calendar Blocking - Time Architecture:
            Morning Block (8-10 AM): Deep Focus Work
            Mid-Morning (10-11 AM): Email & Communication
            Afternoon (2-4 PM): Creative Tasks
            Late Day (4-5 PM): Planning Tomorrow

            Color Code Your Calendar:
            🔵 Deep Work
            🟢 Meetings
            🟡 Admin Tasks
            🔴 Breaks""",

            'e': """🎯 Distraction Audit - Track Your Focus Destroyers:
            Step 1: Log every interruption for one day
            Step 2: Categorize them (notifications, people, noise)
            Step 3: Create solutions for top 3 distractions

            Common Solutions:
            • Put phone in another room
            • Use website blockers
            • Wear noise-canceling headphones"""
        }
        return techniques.get(technique, "Technique not found")

    def get_social_media_challenge(self) -> str:
        """Returns a random social media reality check challenge."""
        challenges = [
            """24-Hour Digital Detox Challenge:
            → No social media for 24 hours
            → Use this time for analog activities
            → Notice how your mind feels clearer
            → Track what you accomplished instead""",

            """Compare Time vs. Value Test:
            → Check your screen time stats
            → List what you gained from each hour
            → Rate each platform's value (1-10)
            → Delete apps scoring below 5""",

            """Mindful Scroll Test:
            → Before opening any social app, ask:
               "What am I looking for?"
            → Set a 5-minute timer
            → Close the app when it rings
            → Write down if you found what you needed""",

            """Notification Fasting:
            → Mute all non-essential apps for 48 hours
            → Keep only calls & messages
            → Experience the mental clarity
            → Notice improved focus""",

            """1 App, 1 Hour Rule:
            → Choose ONE social platform per day
            → Limit usage to 1 hour
            → Use a timer to stay honest
            → Log what you miss (probably nothing!)"""
        ]
        return random.choice(challenges)

    def get_smart_response(self, user_input: str, current_menu: str = "main") -> str:
        """
        Generates detailed responses based on numbered menu selection.
        Now with implementation guides and practical examples!
        """
        self.interaction_count += 1

        try:
            choice = int(user_input)
            if choice == 1:
                return self.get_focus_tip()
            elif choice == 2:
                activity = self.get_random_activity()
                return f"\n🌟 Offline Adventure Suggestion:\n{activity}\n\n→ Getting Started: Set a specific time today\n→ Duration: 30-60 minutes\n→ Benefits: Reduced screen fatigue, increased creativity"
            elif choice == 3:
                remaining = self.screen_time_goal - (self.interaction_count * 0.05)  # Rough estimate
                return f"\n🎯 Screen Time Progress:\n• Daily Goal: {self.screen_time_goal} hours\n• Estimated Usage: {self.interaction_count * 0.05:.1f} hours\n• Remaining: {max(0, remaining):.1f} hours\n\n→ Remember: Quality over quantity!"
            elif choice == 4:
                return self.show_menu("productivity")
            elif choice == 5:
                challenge = self.get_social_media_challenge()
                return f"\n📱 Social Media Reality Check Challenge:\n{challenge}\n\n→ Ready to level up your digital wellness?"
            elif choice == 6:
                return f"\n📊 Digital Wellness Summary:\n• Interactions Today: {self.interaction_count}\n• Mindful Moments: {len(self.activity_history)}\n• Current Mood: {self.last_mood}\n\n→ Keep going, {self.user_name}! Every mindful choice counts."
            elif choice == 7:
                return self.read_and_focus_image("user_image.jpg")
            elif choice == 8:
                self.running = False
                return f"✨ Farewell, {self.user_name}! Your journey to digital wellness continues offline."
            else:
                return f"\n❓ Please choose a number between 1-7\n{self.show_menu()}"
        except ValueError:
            return f"\n❓ Please enter a number to select an option\n{self.show_menu()}"

    def run(self):
        """
        The main show - where digital wellness meets friendly guidance!
        """
        # Welcome message (first impressions matter!)
        print("✨ Welcome to Digital Minimalism Assistant ✨")
        print("🌟 Let's make technology work for you, not the other way around! 🌟")

        # Get to know you (the human behind the screen)
        self.user_name = input("👋 What shall I call you? ").strip()
        print(f"\n🎉 Welcome aboard the digital wellness journey, {self.user_name}! 🎯")

        # Set mindful limits (because boundaries are healthy)
        while not self.screen_time_goal:
            try:
                hours = float(input("⏰ What's your ideal daily screen time target (in hours)? "))
                if 0 < hours <= 24:
                    self.screen_time_goal = hours
                    print(f"📱 Excellent choice! {hours} hours of intentional screen time it is!")
                else:
                    print("❌ Let's keep it real - between 0 and 24 hours, please!")
            except ValueError:
                print("❌ Numbers only, friend! Let's try again.")

        # Set reminder frequency (gentle nudges, not digital nagging)
        while not self.reminder_interval:
            try:
                mins = int(input("⏱️ How often should I remind you to take mindful breaks (in minutes)? "))
                if 1 <= mins <= 60:
                    self.reminder_interval = mins
                    print(f"✅ Roger that! A mindful nudge every {mins} minutes coming right up!")
                else:
                    print("⚠️ Let's keep it between 1 and 60 minutes - we want balance, not burnout!")
            except ValueError:
                print("❌ Numbers only - we're digital minimalists, not magicians!")

        # Start the reminder thread (your personal mindfulness timer)
        reminder_thread = threading.Thread(target=self.start_reminders)
        reminder_thread.daemon = True
        reminder_thread.start()

        # Display welcome message and menu
        print(f"\n🙏 Welcome to your digital wellness journey, {self.user_name}!")
        print("Let's make technology work for you, not the other way around.")
        print(self.show_menu())

        # Main interaction loop with nested menus
        current_menu = "main"
        while self.running:
            if current_menu == "main":
                user_input = input(f"💭 Enter your choice (1-7), {self.user_name}: ").strip()
                if user_input == "2":
                    current_menu = "activities"
                    print(self.show_menu("activities"))
                    continue
                elif user_input == "4":
                    current_menu = "productivity"
                    print(self.show_menu("productivity"))
                    continue
                response = self.get_smart_response(user_input, current_menu)
            else:
                user_input = input("Choose your option: ").strip().lower()
                if user_input == 'r':
                    current_menu = "main"
                    print(self.show_menu())
                    continue
                elif current_menu == "activities":
                    response = self.get_activity_suggestion(user_input)
                    print(response)
                    print("\nReturn to activities menu? (y/n): ")
                    if input().lower() != 'y':
                        current_menu = "main"
                        print(self.show_menu())
                    else:
                        print(self.show_menu("activities"))
                    continue

            print(response)
            if self.running and not response.startswith("✨ Farewell"):
                print("\nWhat's next on your digital wellness journey?")
                if current_menu == "main":
                    print(self.show_menu())


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
assistant = DigitalDetoxAssistant()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start():
    # Initialize assistant data here if needed
    return jsonify({'message': 'Digital Detox Assistant started!', 'data': {'name': assistant.user_name, 'goal': assistant.screen_time_goal}})


# Gunicorn configuration
if __name__ == "__main__":
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(host='0.0.0.0', port=5000, debug=True)
        
