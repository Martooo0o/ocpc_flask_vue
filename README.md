----No Docker, No Kubernetes start(used for development)----

Starting Flask service: 
0.Go to service/OCPC

(FAST START WITH SCRIPT) Use this script to just skip steps 1-3
       
    $ chmod +x start_dev.sh; ./start_dev.sh

(IF NOT USING start_dev.sh)

1.Activate the virtual environment

    $ source myenv/bin/activate

2.Set environment variables:

    $ export FLASK_ENV=development; export FLASK_APP=FLASK_APP

3.Start flask app:

    $ flask run --host=localhost

   Flask backend will be running on http://localhost:5000

4.If the database hasn't been created yet then run:

Open python shell:

    $ python

And import the database and app variables:

    $ from manage.py import my_app
    $ from app import db

Create database:

    $ with my_app.app_context:\
    $   db.create_all()

Starting Vue service:
0.Go to services/ocpc_vue_frontend
1.Start:

    $ npm run serve

----------Only Docker-Compose, No Kubernetes Build----------

Build/run container from image: 
1.Go to root project directory

2.Run command: 

    $ docker-compose up -d --build

3.Create DB:
   
    $ docker-compose exec web python manage.py create_db 

Stop Containers:

    $ docker-compose stop
    $ docker-compose rm -f -v

----------Local Kubernetes build with 'minikube'

1. Install minikube if not installed:

---To be added

2. Create a cluster on local machine:

$ minikube start
$ minikube dashboard

3. Create Docker images if not yet created. every time there is a change those need to be updated.

$ docker build -t marto0o/flask-ocpc ./services/OCPC
$ docker push marto0o/flask-ocpc

$ docker pull marto0o/flask-ocpc

And repeat thi process for Vue as well, but in this case we also specify the file, because we're setting a specific domain for the root API unlike when running only on Docker. 
$ docker build -t marto0o/ocpc-vue ./services/ocpc_vue_frontend -f ./services/ocpc_vue_frontend/Dockerfile-minikube
$ docker push marto0o/ocpc-vue

$ docker pull marto0o/ocpc-vue

5. Initialise cluster

$ sh deploy.sh

4. Next, you need to update your /etc/hosts file to route requests from the host we defined, 'ocpcubes', to the Minikube instance.
Add an entry to /etc/hosts:

$ echo "$(minikube ip) ocpcubes" | sudo tee -a /etc/hosts

5. Create db: 

$ docker 