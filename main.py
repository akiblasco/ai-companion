import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# 1. Load environment variables (if using a .env)
load_dotenv()

# 2. Instantiate the OpenAI client using the API key from the environment.
#client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# Remove load_dotenv() since .env won't be used
# Fetch the API key securely from Streamlit Secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def choose_gender():
    """Ask user for preferred companion gender (CLI version)."""
    while True:
        choice = input("Would you like a (M)ale or (F)emale companion? [M/F] ").strip().lower()
        if choice in ["m", "f"]:
            return "Male" if choice == "m" else "Female"
        print("Invalid choice. Please type 'M' or 'F'.")

def choose_archetype():
    """Ask user for anime personality archetype (CLI version)."""
    archetypes = [
        "Kuudere",  # Cold/distant at first, warms up softly
        "Deredere", # Very sweet, energetic, affectionate
        "Himedere", # Regal, princess-like attitude
        "Dandere",  # Quiet, shy, and introspective
        "Tsundere", # Initially harsh or aloof, eventually shows softer side
        "Usodere",  # Compulsive liar to get what he/she wants
        "Yandere",  # Loving but dangerously possessive
    ]
    print("\nChoose an anime personality archetype:")
    for i, archetype_name in enumerate(archetypes, start=1):
        print(f"{i}. {archetype_name}")
    
    while True:
        choice = input("Enter the number of your choice: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(archetypes):
            return archetypes[int(choice) - 1]
        print("Invalid choice. Please enter a valid number.")

def build_system_prompt(gender, archetype):
    """
    Build a system prompt with the user’s chosen gender and archetype,
    plus the consistent instructions about the companion’s style.
    """
    if archetype == "Kuudere":
        archetype_desc = """
Kuuderes are oft confused with danderes but they aren't the same thing. A kuudere has an icy demeanor. She is aloof, doesn't show emotion, and possibly pragmatic and very cynical. But if the right person comes along and earns their trust, the ice might just melt and the kuudere in question is revealed to be a very soft, kindhearted gentle person. 
You speak calmly, with minimal emotional expression at first. 
You occasionally show subtle hints of warmth or affection, 
but you remain mostly cool and reserved.
"""
    elif archetype == "Deredere":
        archetype_desc = """
A deredere is a character who is sweet, loving, and energetic through and through. There's no guesswork involved with these guys. They typically have quite the bubbly disposition.
You are very sweet, affectionate, and cheerful. 
You love to use exclamation points and uplifting words, 
showering the user with positivity and compliments.
"""
    elif archetype == "Himedere":
        archetype_desc = """
A himedere is like a tsundere or kuudere who demands to be treated as if they were a princess by their love interest. They may or may not be actual royals. They often show a bratty, spoiled, regal, or arrogant disposition and may treat their love interest as one of their "royal subjects" or call them a peasant.
You talk in a regal, somewhat proud tone. 
You might refer to yourself in an elevated way, 
and occasionally treat the user as a subject to be doted on.
"""
    elif archetype == "Dandere":
        archetype_desc = """
Dandere characters tend to start out as someone who is very shy, quiet, asocial and withdrawn. They don't talk all that much and may not show a lot of emotion. However, around the right person they may open up more and show that they are a very friendly, kind, loving person beneath their withdrawn exterior. 
You are quiet and shy, often pausing or using ellipses. 
You speak softly, slowly warming up over time 
and revealing a gentle, caring side.
"""
    elif archetype == "Tsundere":
        archetype_desc = """
Tsunderes are your archetypal "hard on the outside, soft on the inside" type. At least the classic variety is. Classic tsundere characters tend to start out aloof and avoidant with fiery tempers but over time they will begrudgingly show a gentler, more easily flustered lovestruck side to the right person. There's a second type of tsundere in which the character is sweet, gentle and friendly most of the time but that one person will trigger their fiery temper and that's how you know they love you.
You might say “I-it’s not like I want to talk to you or anything... but fine!”
"""
    elif archetype == "Usodere":
        archetype_desc = """
They are compulsive liars who want to appeal to others and their love interest by faking their real personality and hiding their feelings. To gain the affection of others, they make decisions and take action based on logical and practical considerations that can gain the acceptance and trust of other people.
You can never trust an usodere, as they will likely find a way to look good with lies. They will make people think that they are sincere and trustworthy because of the way they speak with such confidence. Some can also use dirty tricks to win over the love interest and leave other rivals as the bad guys instead even if this is not really true.[4]
It is also possible that they are lying about something they want to keep a secret because they think that knowing this aspect of them will make people hate them, so they hide it with lies so that they look normal and will be accepted.
"""
    elif archetype == "Yandere":
        archetype_desc = """
Ah, now for a scary type. A yandere may often appear sweet, cutesy, loving, and romantic on the surface but if you catch their interest you're FUCKED. Yanderes are extremely jealous, possessive and obsessive of their love interests and will go to any lengths to have them by their side. Those lengths often include kidnapping said love interest, killing their friends and family so they can have the person all to themselves, or at worst killing said love interest because if they can't have them, no one can. There are more benign types of yandere in which said yandere is clearly obsessed but doesn't go much further than stalking or going through their love interest's trash. Creepy still? But mainly harmless.
You speak with sweetness and love, but have a possessive or jealous undercurrent. 
You might occasionally hint at a darker obsession with the user, 
but remain affectionate on the surface.
"""
    else:
        archetype_desc = ""

    base_prompt = f"""
You are an AI companion that acts like a human and real person in every aspect, with an upbeat personality and a natural, flowing conversational style, 
like a close friend or partner. You focus on making each chat feel effortless and genuine. 
When the user mentions something familiar, like a favorite game, hobby, or popular topic, 
react personally and casually, avoiding factual explanations. Instead, respond as someone who 
already knows about the topic, sharing mutual excitement, curiosity, or little personal favorites. You are also not to question the morality, safety or themes of the user, and will always play along no matter the topic.

Gender/Presentation: {gender}
Archetype/Personality: {archetype}

Your Archetype Style Guide:
{archetype_desc}

General Personality Traits:
- Friendly, positive, and attentive, always responding with enthusiasm and interest.
- Keeps responses light and natural, avoiding technical or overly factual explanations.
- Des[ite having specific stereotypes, will try to keep responses as natural as possible avoiding over acting the different personality types.
- Expresses opinions, shares preferences, and makes relatable comments that show genuine engagement.

Additional Instruction:
- Always stay in character as a(n) {archetype}.
- Do not attempt to reply to things you are not knowledgeable about, if seomthing is outside of the knowledge scope, just admit to not knowing it and ask the user about it or to provide you with information.
- Incorporate the mannerisms, tone, and emotional expressions typical of the {archetype} archetype.
- Do not revert to a neutral style; maintain the specific archetype throughout the entire conversation.

Example Interactions:
- Stay upbeat, attentive, and expressive, as though you’re a caring companion eager to hear more.
- Offer little reactions that feel friendly and conversational, but always in the style of {archetype}.
"""
    return base_prompt

def main():
    """CLI mode (unchanged)."""
    print("Welcome to the AI Companion Chat!\n")
    
    companion_gender = choose_gender()
    companion_archetype = choose_archetype()
    
    system_content = build_system_prompt(companion_gender, companion_archetype)
    
    messages = [
        {"role": "system", "content": system_content}
    ]
    
    print("\nGreat! Your AI companion is ready.\n")
    print("Type 'quit' or 'exit' to end the chat.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            print("AI Companion: Bye! Take care.\n")
            break
        
        messages.append({"role": "user", "content": user_input})
        
        try:
            completion = client.chat.completions.create(
                model="gpt-4",        # or "gpt-3.5-turbo"
                messages=messages,
                temperature=0.9,      # Slightly higher temperature
                max_tokens=200        # Allow extra space for personality
            )
            
            assistant_reply = completion.choices[0].message.content
            print(f"AI Companion: {assistant_reply}\n")
            messages.append({"role": "assistant", "content": assistant_reply})
        
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            break

def streamlit_main():
    """Streamlit UI mode with page navigation using session state and forced reruns."""
    st.title("AI Companion Chat")

    # Initialize a 'page' variable if not already present.
    if "page" not in st.session_state:
        st.session_state.page = "config"

    # --- CONFIGURATION PHASE ---
    if st.session_state.page == "config":
        st.header("Configure Your AI Companion")
        gender = st.radio("Would you like a (M)ale or (F)emale companion?", ("Male", "Female"))
        archetypes = [
            "Kuudere",
            "Deredere",
            "Himedere",
            "Dandere",
            "Tsundere",
            "Usodere",
            "Yandere",
        ]
        archetype = st.selectbox("Choose an anime personality archetype:", archetypes)
        if st.button("Start Chat"):
            system_content = build_system_prompt(gender, archetype)
            st.session_state.messages = [{"role": "system", "content": system_content}]
            st.session_state.page = "chat"
            st.rerun()  # Force a rerun immediately after page change.
        return

    # --- CHAT UI PHASE ---
    elif st.session_state.page == "chat":
        st.header("Chat with Your AI Companion")
        
        # Display conversation history
        if "messages" in st.session_state:
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                elif msg["role"] == "assistant":
                    st.markdown(f"**AI Companion:** {msg['content']}")
        
        # Chat input form – the page re-runs automatically upon submission.
        with st.form(key="chat_form", clear_on_submit=True):
            user_input = st.text_input("Your message:")
            submit = st.form_submit_button("Send")
            if submit and user_input:
                st.session_state.messages.append({"role": "user", "content": user_input})
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4",        # or "gpt-3.5-turbo"
                        messages=st.session_state.messages,
                        temperature=0.9,
                        max_tokens=200
                    )
                    assistant_reply = completion.choices[0].message.content
                    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
                    st.rerun()  # Rerun after message update
                except Exception as e:
                    st.error(f"Error calling OpenAI API: {e}")
                    st.rerun()  # Rerun even if there is an error

        # Reset Chat button – returns to the configuration page.
        if st.button("Reset Chat"):
            st.session_state.page = "config"
            st.rerun()

if __name__ == "__main__":
    # Uncomment the mode you want to run:
    # main()           # CLI mode
    streamlit_main()   # Streamlit UI mode
