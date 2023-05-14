# meeting_room_occupancy

## Install submodule
```
git submodule update --init
```

## Build images
```
docker compose up -d --build
```

## Add data
```
curl --header "Content-Type: application/json" --request POST --data '{"sensor":"cbd","ts":"2018-11-14T13:34:49Z","in":3,"out":2}' http://127.0.0.1:5000/api/webhook
```

## Front end 
```
http://127.0.0.1:8080/occupancy
```