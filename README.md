# SPMG3T6_Github Set-Up/Accessing Application Instructions

(To access it locally. For deployment, you just need to visit the deployment link.)

Please ensure port 3000 and port 8000 are not in use as they are the ports to be used for our frontend and backend applications.

## For Frontend ReactJs Application:

1. Unzip the zipped source files and open the folder in VSCode or navigate to its directory in the command line/cmd.
2. Type `cd frontend` in the terminal (VSCode terminal/command line).
3. In the terminal, type:
   ```sh
   npm install
   ```
   (to install all dependencies)
   
   To install dependencies separately, type in the terminal:
   ```sh
   npm i devextreme-react
   npm install react-datepicker
   npm install react-router-dom
   ```
4. To run the frontend application, type in the terminal:
   ```sh
   npm run start
   ```

## For Backend Flask Application:

1. Install Supabase for connection to Supabase:
   ```sh
   pip install supabase
   ```
2. Install the coverage tool:
   ```sh
   python3 -m pip install coverage
   ```
3. Install pytest for unit tests:
   ```sh
   pip install -U pytest
   ```
4. Install Flask for the backend application:
   ```sh
   pip install flask
   ```
5. To run the backend Flask application, open another terminal and type:
   ```sh
   cd backend
   python app.py
   ```
