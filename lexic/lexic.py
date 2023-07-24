from variables import mngr

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
                 'We are collecting selfies of real people. '
                 'Your picture and personal data will not be published anywhere, '
                 'our purpose is training neural networks to distinguish parts of faces.'
                 'We will check your file and give you the verification code.\n\n'
                 'Please read our privacy policy by the button below and press ✅ button to continue.',

        'ban': f'You were banned',

        'help': f'If something does not work, try again /start or contact {mngr}',

        'instruct1': 'Thanks! Please now see the examples and instruction.',
        'instruct2': 'Instructions:\n'
                     '\n1. The insurance card must be completely on the photo, it must not be cropped.'
                     '\n2. Photos must be of good quality, clear, without blurring, the data on the insurance card must be clearly visible.'
                     '\n3. The card must lie on a flat surface, you can not take a picture holding it in your hand.'
                     '\n4. The insurance card should have no shadows of anything, the lighting should be even.'
                     '\n5. The insurance card should not have glare from too bright lighting.'
                     '\n6. The insurance card must not be damaged or dirty. The card must be of good quality.'
                     '\n7. Please make sure both front and back of the card are mapped to one person/id/card. Nothing should be redacted on the back of the card.'
                     '\n8. The image should be clear and readable. There should not be any light reflection on the final image.'
                     '\n9. The age of the document should be 2010+ (card should not have been issued before 2010).'
                     '\n10. All images should be real, from the real participants, not downloaded from the internet.'
                     '\n11. No photocopies are allowed.'
                     '\n12. Virtual insurance cards are not allowed.'
                     '\n',


        'instruct3': 'You can now send your pictures. Please send each file in two separate messages, not as one album.',

        'example_link': 'https://storage.yandexcloud.net/sbs-toloka/rr/insurance_cards/example_correct_1.jpg',
        'log': 'med_done'

    },
}
