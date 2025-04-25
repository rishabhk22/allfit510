# AllFit - Personalized Workout Plans

## Project Description
AllFit is a user-friendly web application that creates personalized workout plans by blending different fitness methods such as yoga, weight training, cardio, calisthenics, and stretching. It enables users to have a holistic fitness routine to improve different aspects of their health.

## Features
- User authentication (registration and login)
- Personalized workout plan generation
- Progress tracking
- Responsive and modern UI
- Multiple fitness methods integration

## Quick Start

### For Unix/Linux/macOS Users:
```bash
# Clone the repository
git clone https://github.com/rishabhk22/allfit510.git
cd allfit510

# Make the scripts executable
chmod +x setup.sh run_allfit.sh

# Run the application (this will handle setup automatically on first run)
./run_allfit.sh
```

### For Windows Users:
```bash
# Clone the repository
git clone https://github.com/rishabhk22/allfit510.git
cd allfit510

# Run the application (this will handle setup automatically on first run)
run_allfit.bat
```

The application will be available at: http://localhost:5000

## Manual Setup (Alternative)

If you prefer to set up manually, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/rishabhk22/allfit510.git
cd allfit510
```

2. Create and activate a virtual environment:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
# Create a .env file in the root directory
touch .env  # On Windows: type nul > .env
```

Add the following to your .env file:
```
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///allfit.db
```

5. Initialize the database:
```bash
# Create the database directory
mkdir -p instance

# Initialize the database
flask db init
flask db migrate
flask db upgrade
```

6. Run the application:
```bash
# Development mode
flask run

# Or using the run script
python run.py
```

## Project Structure
```
allfit510/
├── app/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/
│   ├── models/
│   ├── routes/
│   └── forms/
├── instance/           # Database and instance-specific files
├── venv/              # Virtual environment
├── .env               # Environment variables
├── .env.example       # Example environment variables
├── .gitignore         # Git ignore file
├── requirements.txt   # Python dependencies
├── run.py            # Application entry point
├── test_app.py       # Test suite
├── setup.sh          # Setup script (Unix/Linux/macOS)
├── setup.bat         # Setup script (Windows)
├── run_allfit.sh     # Run script (Unix/Linux/macOS)
├── run_allfit.bat    # Run script (Windows)
└── README.md         # Project documentation
```

## Progress
- [x] Project structure setup
- [x] Virtual environment configuration
- [x] Basic Flask application setup
- [x] User authentication system
- [x] Database models for users and workout plans
- [x] Basic UI templates
- [x] Responsive design implementation
- [ ] Workout plan generation algorithm
- [ ] Progress tracking dashboard
- [ ] Exercise database integration
- [ ] User profile management
- [ ] Workout plan customization
- [ ] Mobile app integration (future)

## Technologies Used
- Python 3.x
- Flask
- SQLAlchemy
- Bootstrap 5
- JavaScript
- HTML5/CSS3

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact
- Project Manager: Rishabh Kumar – rkumar23@uw.edu
- Lead Developer: Shareef Jasim – shareef.abdulnafaa@gmail.com

## Project Objectives
To evelop a user-friendly web-app to create personalized workout plans by blending different fitness methods or exercise types such as yoga, weight training, cardio, calisthenics, and stretching. This is to enable users to have a holistic fitness routine to improve different aspects of their health such as strength, mobility, flexibility, endurance to provide balanced overall fitness. 

## Target
Busy professionals with some experince in workout or fitness traning that want to diversify their fitness routine to be more holistic.

## Primary Needs
- Customization based on goals (such as build strength, increase flexibility, etc.)
- Clear day-wise breakdown of exercise or fitness method
- Time-efficient routines

## Key Deliverables
- Interactive web app interface where users can input their details, goals, and requirements for a fitness plan with their focus
- User onboarding flow with goal selection and fitness level input
- Short details about the workout suggested
- Workout plan generator combining various training types

### Good-to-have
- Steps for workout and how to do it (can be visual or text)
- Progress tracking dashboard

## Special Constraints
- Take user consent before suggesting the workout and physical activity
- Clearly communicate with disclaimers and warnings that fitness advice is non-medical and should be followed at the user's own discretion

## Expected Outcome
- Interactive web app that can run on desktop seamlessly and be accessed from anywhere in the world
- A personalized, flexible, and holistic workout solution that gives the correct fitness routine as per user requirements and that users trust and enjoy engaging with

## Initial UI 
![alt text](https://github.com/rishabhk22/allfit510/blob/main/image.png "Initial UI")


## Timeline

| **Week**   | **Milestone**                    | **Expectation**                                                                 |
|----------|----------------------------------|----------------------------------------------------------------------------------|
| Week 1   | Planning & Research              | Define MVP, user personas, feature list, and tech stack                         |
| Week 2   | Wireframes & Architecture        | Create wireframes, app structure, and development setup                         |
| Week 3   | Onboarding & User Input Flow     | Build onboarding flow and capture user goals/preferences                        |
| Week 4   | Workout Plan Generator           | Develop logic for generating personalized weekly plans                          |
| Week 5   | UI Design & Content Integration  | Apply design, visuals, and workout content (GIFs/videos)                        |
| Week 6   | Testing & Progress Tracking      | QA testing, bug fixes, and add progress tracking features                       |
| Week 7   | Launch Preparation               | Set up hosting, landing page, legal disclaimers, and analytics                  |
| Week 8   | Soft Launch & Feedback           | Beta release, gather feedback, fix issues, and plan next iteration              |

## Challenges:
- Images and possible short videos to make it visual
- Best way to take user input for preferences
- Test for suitability of the workouts
- Accurately match time-slot and workout durations

## Contact Information

- **Project Manager:** Rishabh Kumar  – rkumar23@uw.edu – [GitHub: rishabhk22](https://github.com/rishabhk22)
- **Lead Developer and UX/UI Designer:** Shareef Jasim – shareef.abdulnafaa@gmail.com – [GitHub: shareefjasim](https://github.com/shareefjasim)






