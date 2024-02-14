from flask import Flask, request, Response
import json, boto3

app = Flask(__name__)
sqs = boto3.resource('sqs')
low_queue = sqs.get_queue_by_name(QueueName='Low')
medium_queue = sqs.get_queue_by_name(QueueName='Medium')
high_queue = sqs.get_queue_by_name(QueueName='High')
queue_dict = {
    "Low": low_queue,
    "Medium": medium_queue,
    "High": high_queue
}

@app.route('/', methods=["POST"])
def API():
    data = json.loads(request.data)
    if len(data) != 0:
        print(data)
        body = {
            "title": data["title"],
            "description": data["description"]
            }
        
        response = queue_dict[data["priority"]].send_message(MessageBody=json.dumps(body))

        if response.get('ResponseMetadata')['HTTPStatusCode'] == 200:
            return Response("Successfully added to the queue.", status=200)
        
        return Response("Unsuccessful adding message to queue.", status=500)
    
    return Response("Data is required.", status=400)

if __name__ == "__main__":
    app.run()
