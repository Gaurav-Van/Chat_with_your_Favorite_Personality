import streamlit as st


def get_gradient_style():
    return """
    <style>
    .gradient-text {
      font-size: 50px !important;
      font-family: 'Roboto', sans-serif;
      font-weight: bold;
      background: -webkit-linear-gradient(#FF5733, #9400D3, #4B0082);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    </style>
    """


def display_title():
    st.markdown(get_gradient_style(), unsafe_allow_html=True)
    st.markdown("<div class='gradient-text'>CHAT WITH YOUR FAVORITE PERSONALITY</div>", unsafe_allow_html=True)


def display_image():
    st.image('OIP.jpeg', use_column_width=True)


def get_personality_choice():
    option = st.radio("",
                      (
                          'Enter the name of your favorite personality',
                          'Or choose from the list of famous personalities'))
    if option == 'Enter the name of your favorite personality':
        return st.text_input("", key="user_input")
    else:
        famous_personalities = ["", "Socrates", "Cleopatra", "Genghis Khan", "Leonardo da Vinci", "William Shakespeare",
                                "Joan of Arc", "Marie Curie", "Mahatma Gandhi", "Nelson Mandela", "Albert Einstein",
                                "Martin Luther King Jr.", "Alan Turing", "Nikola Tesla", "Alexander Fleming",
                                "Steve Jobs", "Bill Gates", "Tim Berners-Lee", "Ludwig van Beethoven", "Pablo Picasso",
                                "Michael Jackson", "Oprah Winfrey", "Muhammad Ali", "Pele", "Malala Yousafzai",
                                "Barack Obama", "Elon Musk"]
        return st.selectbox("", famous_personalities, key="dropdown")


def main():
    display_title()
    display_image()
    personality = get_personality_choice()
    with open('Personality.txt', 'w') as f:
        f.write(personality)
    if personality:
        st.switch_page("chat.py")


if __name__ == "__main__":
    main()
