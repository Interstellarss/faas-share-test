
from backend_onnxruntime import BackendOnnxruntime
from PIL import Image
import copy
import numpy as np
base_dir = "/tmp/inference/vision/classification_and_detection"
label_name = ['Airplane', 'Antelope', 'Apple', 'Backpack', 'Balloon', 'Banana', 'Barrel', 'Baseball bat', 'Baseball glove', 'Bee', 'Beer', 'Bench', 'Bicycle', 'Bicycle helmet', 'Bicycle wheel', 'Billboard', 'Book', 'Bookcase', 'Boot', 'Bottle', 'Bowl', 'Bowling equipment', 'Box', 'Boy', 'Brassiere', 'Bread', 'Broccoli', 'Bronze sculpture', 'Bull', 'Bus', 'Bust', 'Butterfly', 'Cabinetry', 'Cake', 'Camel', 'Camera', 'Candle', 'Candy', 'Cannon', 'Canoe', 'Carrot', 'Cart', 'Castle', 'Cat', 'Cattle', 'Cello', 'Chair', 'Cheese', 'Chest of drawers', 'Chicken', 'Christmas tree', 'Coat', 'Cocktail', 'Coffee', 'Coffee cup', 'Coffee table', 'Coin', 'Common sunflower', 'Computer keyboard', 'Computer monitor', 'Convenience store', 'Cookie', 'Countertop', 'Cowboy hat', 'Crab', 'Crocodile', 'Cucumber', 'Cupboard', 'Curtain', 'Deer', 'Desk', 'Dinosaur', 'Dog', 'Doll', 'Dolphin', 'Door', 'Dragonfly', 'Drawer', 'Dress', 'Drum', 'Duck', 'Eagle', 'Earrings', 'Egg,(Food)', 'Elephant', 'Falcon', 'Fedora', 'Flag', 'Flowerpot', 'Football', 'Football helmet', 'Fork', 'Fountain', 'French fries', 'French horn', 'Frog', 'Giraffe', 'Girl', 'Glasses', 'Goat', 'Goggles', 'Goldfish', 'Gondola', 'Goose', 'Grape', 'Grapefruit', 'Guitar', 'Hamburger', 'Handbag', 'Harbor seal', 'Headphones', 'Helicopter', 'High heels', 'Hiking equipment', 'Horse', 'House', 'Houseplant', 'Human arm', 'Human beard', 'Human body', 'Human ear', 'Human eye', 'Human face', 'Human foot', 'Human hair', 'Human hand', 'Human head', 'Human leg', 'Human mouth', 'Human nose', 'Ice cream', 'Jacket', 'Jeans', 'Jellyfish', 'Juice', 'Kitchen & dining room table', 'Kite', 'Lamp', 'Lantern', 'Laptop', 'Lavender (Plant)', 'Lemon', 'Light bulb', 'Lighthouse', 'Lily', 'Lion', 'Lipstick', 'Lizard', 'Man', 'Maple', 'Microphone', 'Mirror', 'Mixing bowl', 'Mobile phone', 'Monkey', 'Motorcycle', 'Muffin', 'Mug', 'Mule', 'Mushroom', 'Musical keyboard', 'Necklace', 'Nightstand', 'Office building', 'Orange', 'Owl', 'Oyster', 'Paddle', 'Palm tree', 'Parachute', 'Parrot', 'Pen', 'Penguin', 'Personal flotation device', 'Piano', 'Picture frame', 'Pig', 'Pillow', 'Pizza', 'Plate', 'Platter', 'Porch', 'Poster', 'Pumpkin', 'Rabbit', 'Rifle', 'Roller skates', 'Rose', 'Salad', 'Sandal', 'Saucer', 'Saxophone', 'Scarf', 'Sea lion', 'Sea turtle', 'Sheep', 'Shelf', 'Shirt', 'Shorts', 'Shrimp', 'Sink', 'Skateboard', 'Ski', 'Skull', 'Skyscraper', 'Snake', 'Sock', 'Sofa bed', 'Sparrow', 'Spider', 'Spoon', 'Sports uniform', 'Squirrel', 'Stairs', 'Stool', 'Strawberry', 'Street light', 'Studio couch', 'Suit', 'Sun hat', 'Sunglasses', 'Surfboard', 'Sushi', 'Swan', 'Swimming pool', 'Swimwear', 'Tank', 'Tap', 'Taxi', 'Tea', 'Teddy bear', 'Television', 'Tent', 'Tie', 'Tiger', 'Tin can', 'Tire', 'Toilet', 'Tomato', 'Tortoise', 'Tower', 'Traffic light', 'Train', 'Tripod', 'Truck', 'Trumpet', 'Umbrella', 'Van', 'Vase', 'Vehicle registration plate', 'Violin', 'Wall clock', 'Waste container', 'Watch', 'Whale', 'Wheel', 'Wheelchair', 'Whiteboard', 'Window', 'Wine', 'Wine glass', 'Woman', 'Zebra', 'Zucchini'] 

backend = BackendOnnxruntime()
model = backend.load("/models/retinanet/resnext50_32x4d_fpn.onnx") 
image = Image.open("/workspace/client/car.jpg")
image = image.resize((800, 800))
image = np.array(image).astype(np.float32)
image = image/255.
image = np.moveaxis(image, -1, 0)
image = image[np.newaxis, :]
print(image.shape)
print(model.inputs[0])
num = 0
def issue_once():
    global num
    data = copy.deepcopy(image)
    print("No. %d processing!" % num, flush=True)
    result = model.predict({"images":data})
    print("No. %d processed!" % num, flush=True)
    num = num + 1
    bboxes_ = result[0] 
    scores_ = result[1] 
    labels_ = result[2] 
    labels = [label_name[idx] for idx in labels_]
    result = [bboxes_[:5], labels[:5], scores_[:5]]
    print(result, flush=True)
issue_once()
issue_once()
issue_once()
issue_once()
