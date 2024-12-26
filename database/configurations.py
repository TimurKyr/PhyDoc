from motor.motor_asyncio import AsyncIOMotorClient


uri = "mongodb+srv://kyrbassovtimur:I9H4SvwZgaPUyqjr@cluster0.yndqb.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = AsyncIOMotorClient(uri)
db = client["Messenger"]
