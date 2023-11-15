# The Book Review Hub
## Project Description:
Book Review Platform API with Authentication and RBAC

### Objective:
Developed a RESTful API for a Book Review Platform using Flask. The platform should allow users to post book reviews, rate books, and comment on reviews. It will include user authentication, role-based access control, and advanced functionalities like search and filtering.

--------------------
## Api documentations
    https://documenter.getpostman.com/view/28221885/2s9YXnyyUe
-------

## UML  Diagram
    https://app.eraser.io/workspace/TPJqot4tzjMNqZ16sH3r?origin=share
## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Create a virtual environment:
    ```bash
    python3 -m vev env 
    ```

3. activate  virtual environment:
    ```bash
    source env/bin/activate

    on windows
    
    env\Scripts\activate
    ```

4. install dependencies::
    ```bash
    pip install -r requirements.txt
    ```

5. Initialize the database:::
    ```bash
    flask shell
    ```
    ```bash
    db.create_all()
    ```

6. Run the Flask app:
    ```bash
    flask run
    ```
