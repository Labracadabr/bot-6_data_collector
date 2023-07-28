from settings import mngr

# RU: dict[str, dict[str, str]] = {}
EN: dict[str, dict[str, str]] = {
    'selfie': {

        'start': 'Hi!\n\n'
                 'We are collecting selfies of real people. '
                 'Your picture and personal data will not be published anywhere, '
                 'our purpose is training neural networks to distinguish parts of faces.'
                 'We will check your file and give you the verification code.\n\n'
                 'Please read our privacy policy by the button below and press ✅ button to continue.',

        'ban': f'You were banned',

        'full_hd': 'You must send pictures as files <b>without compression</b>. If you do not know how,'
                   ' <a href="https://www.youtube.com/embed/qOOMNJ0gIss">here</a> is a 9 sec tutorial.',

        'help': f'If something does not work, contact {mngr}',

        'instruct1': 'Thanks! Please now see the examples and instruction.',
        'instruct2': 'Instructions:\n'
                     '- First of all - wipe your camera lens :)\n'
                     '- The face should be clearly visible (in focus, NOT blurred, in good light)\n'
                     '- The head should be completely in the frame (NOT cropped)\n'
                     '- The face must be completely open (NOT covered with a mask/hands/sunglasses or anything else).',
        'instruct3': 'You can now send your picture.',
        'example_link': 'https://i.ibb.co/z89YvcS/collage.jpg',
        'log': 'selfie_done'

    },
    'med': {

        'start': 'Hi!\n\n'
                 'We collect data for training neural networks. '
                 'Your personal data will not be used nor published anywhere. '
                 'We will check your response and give you the verification code.\n\n'
                 'Please read our privacy policy by the button below and press ✅ button to continue.',

        'ban': f'You were banned',

        'full_hd': 'You must send pictures as files <b>without compression</b>. If you do not know how,'
                   ' <a href="https://www.youtube.com/embed/qOOMNJ0gIss">here</a> is a 9 sec tutorial.',

        'help': f'If something does not work, try again /start or contact {mngr}',

        'instruct1': 'Thanks! Please now see the examples and instruction.',
        'instruct2': 'Instructions:\n'
                     '\n1. The insurance card must be completely in the photo, not cropped.'
                     '\n2. Photos must be of good quality, clear, without blurring,'
                     ' the data on the insurance card must be clearly visible.'
                     '\n3. <b>The card must lie on a flat surface</b>,'
                     ' you can not shoot it holding it in your hand.'
                     '\n4. The insurance card should not have shadows or glare from too bright lighting.'
                     '\n5. The insurance card must not be damaged or dirty. The card must be of good quality.'
                     '\n6. Card must be <b>issued in 2010 or LATER.</b>'
                     '\n7. All images should be real, from the real participants, not downloaded from the internet -'
                     ' we already have those in our database.',

        'instruct3': 'You can now send your pictures.\n\n'
                     'Please send each file in <b>two separate messages</b>, not as one album.',

        'example_link': 'https://storage.yandexcloud.net/sbs-toloka/rr/insurance_cards/example_correct_1.jpg',
        'example_link2': 'https://storage.yandexcloud.net/sbs-toloka/rr/insurance_cards/example_correct_n2.jpg',
        'example_json': """
    [
        {
            "type": "photo",
            "media": "https://storage.yandexcloud.net/sbs-toloka/rr/insurance_cards/example_correct_1.jpg",
            "caption": "Example"
        },
        {
            "type": "photo",
            "media": "https://storage.yandexcloud.net/sbs-toloka/rr/insurance_cards/example_correct_n2.jpg",
            "caption": "Example"
        }
    ]
    """,
        'log': 'med_done'

    },
}
