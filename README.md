# reflection
This is a really basic data storage API which I created to support building web prototypes.  

It is packaged as a Docker container.

## Starting it

```bash
docker run -p 80:8080 richardjkendall/reflection
```

This will start the server on port 80 of your machine.  Information you send to it will be saved inside the container

## Saving data outside the container

The data is stored in the `/data` volume.  If you want to save this data outside of the container then mount the volume as follows:

```bash
docker run -v <host path>:/data:rw -p 80:8080 richardjkendall/reflection
```

# How it works

## Saving data

The tool expects the first part of the path to be the name of the object being saved.  When saving data for an object you execute a PUT to the object name e.g.

http://[endpoint]/[object]

e.g. using curl

```bash
curl -X PUT -H "content-type: application/json" -d @datafile.json http://[endpoint]/[object]
```

The PUT method returns the ID along with a copy of the data that has been saved for that object.  The ID is a UUID which is automatically assigned.

A HTTP 400 is returned if the request is not well formed JSON.

## Listing data

Issuing a get to the object name will list all the objects of that type which are saved along with their IDs.  e.g.

```bash
curl http://[endpoint]/[object]
```

If you want to return all the data for each object then add the `return_attributes=true` query string e.g.

```bash
curl http://[endpoint]/[object]?return_attributes=true
```

A HTTP 404 is returned if there are no objects found for this object name.

## Getting an object

You can get a specific object by issuing a GET request for the object e.g.

```bash
curl http://[endpoint]/[object]/[id]
```

## Updating an object

You can update a specific object by issuing a POST or PATCH for the object e.g.

```bash
curl -X PATCH -H "content-type: application/json" -d @datafile.json http://[endpoint]/[object]/[id]
```

This will merge the changes in the payload you submit with the data that is already stored.  A HTTP 400 error will be returned if the request is not well formed JSON.  
A HTTP 404 will be returned if the object is not found.

## Replacing or creating a specific object

You can create or replace an object with a given ID by issuing a PUT request for that specific ID.  This will replace all the content current stored for that ID with the new content you have sent.  E.g.

```bash
curl -X PUT -H "content-type: application/json" -d @datafile.json http://[endpoint]/[object]/[id]
```

This will return a HTTP 400 error if the request is not well formed JSON.
