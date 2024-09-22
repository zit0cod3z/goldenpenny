import pandas as pd
from django.core.management.base import BaseCommand
from qr_app.models import Attendee, Child  # Adjust your model imports

class Command(BaseCommand):
    help = 'Import data from an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='The path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        # Read the Excel file
        df = pd.read_excel(file_path)

        # Strip whitespace from column names
        df.columns = df.columns.str.strip()

        # Print column names for debugging
        print("Column names in the DataFrame:", df.columns.tolist())

        # Strip whitespace from string values in the DataFrame
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # Combine first and last name into a single 'name' column
        if 'firstname' in df.columns and 'lastname' in df.columns:
            df['name'] = df['firstname'] + ' ' + df['lastname']

        # Identify duplicates and process unique entries
        unique_df = df.drop_duplicates(subset='phonenumber', keep='first')

        for index, row in unique_df.iterrows():
            email = row.get('email')
            name = row.get('name')
            ticket_type = row.get('ticketTypes')
            phone_number = row.get('phonenumber')
            instagram_handle = row.get('instagram')

            print(f"Processing row {index + 1}: {row.to_dict()}")  # Debugging output

            if email and name:  # Check both email and name are provided
                if phone_number:
                    try:
                        # Check for existing attendee by email
                        attendee, created = Attendee.objects.get_or_create(
                            email=email,
                            defaults={'phone_number': phone_number, 'name': name, 'ticket_type': ticket_type, 'instagram_handle': instagram_handle, }
                        )
                        if not created:
                            attendee.instagram_handle = row.get('instragram', '')
                            attendee.save()
                            self.stdout.write(self.style.SUCCESS(f'Updated attendee: {attendee.name}'))
                        else:
                            # Update existing record if needed
                            attendee.phone_number = phone_number
                            attendee.name = name
                            attendee.ticket_type = ticket_type
                            attendee.instagram_handle = instagram
                            attendee.save()  # Save changes
                            print(f'Updated existing attendee: {attendee.name}')

                    except Exception as e:
                        print(f"Error processing phone number {phone_number}: {e}")

                # Handle Child creation based on available child columns
                for i in range(1, 5):  # Assuming you have child1_name to child4_name
                    child_name = row.get(f'child{i}_name')
                    if isinstance(child_name, str) and child_name.strip():  # Check if it's a string and not empty
                        Child.objects.get_or_create(attendee=attendee, name=child_name.strip())

            else:
                self.stdout.write(self.style.WARNING(f'Skipped row {index + 1}: Missing email or name.'))

        self.stdout.write(self.style.SUCCESS('Data import process completed!'))