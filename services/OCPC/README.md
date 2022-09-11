# OCPC
Object-Centric Process Cubes

# Run app with Gunicorn  
gunicorn -b 0.0.0.0:5000 manage:app\
    --workers 4 \
    --bind 0.0.0.0:9000 \
    --log-file /app/logs/gunicorn.log \
    --log-level DEBUG \
    --reload
