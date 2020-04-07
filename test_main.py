
from app.move_snake import get_move

if __name__ == '__main__':

	#data = {"game": {"id": "5a46bdde-0190-4769-8430-50dce56bd746"}, "turn": 41, "board": {"height": 11, "width": 11, "food": [{"x": 1, "y": 0}], "snakes": [{"id": "gs_YpY8wRY37b6CpyCxHjk7d8yK", "name": "Dunno", "health": 83, "body": [{"x": 4, "y": 3}, {"x": 4, "y": 4}, {"x": 5, "y": 4}, {"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}], "shout": ""}, {"id": "gs_vQFxgrCCTrddwxXcbfK3TWRM", "name": "Cool_as_ice", "health": 80, "body": [{"x": 3, "y": 2}, {"x": 3, "y": 3}, {"x": 2, "y": 3}, {"x": 2, "y": 2}], "shout": ""}, {"id": "gs_r8DcWqCXQDfwVdVwDkJk6t99", "name": "Dragonborn", "health": 96, "body": [{"x": 3, "y": 6}, {"x": 2, "y": 6}, {"x": 1, "y": 6}, {"x": 0, "y": 6}, {"x": 0, "y": 7}, {"x": 1, "y": 7}, {"x": 2, "y": 7}, {"x": 3, "y": 7}], "shout": ""}, {"id": "gs_QCMrDxJvTQrRgk8XRwtvt8p3", "name": "shielded-woodland", "health": 93, "body": [{"x": 3, "y": 4}, {"x": 2, "y": 4}, {"x": 1, "y": 4}, {"x": 1, "y": 5}, {"x": 0, "y": 5}], "shout": ""}]}, "you": {"id": "gs_QCMrDxJvTQrRgk8XRwtvt8p3", "name": "shielded-woodland", "health": 93, "body": [{"x": 3, "y": 4}, {"x": 2, "y": 4}, {"x": 1, "y": 4}, {"x": 1, "y": 5}, {"x": 0, "y": 5}], "shout": ""}}
	data = {"game": {"id": "a82b77d8-b3a3-461d-b865-74e5635d063e"}, "turn": 160, "board": {"height": 11, "width": 11, "food": [{"x": 2, "y": 1}, {"x": 2, "y": 0}, {"x": 5, "y": 10}], "snakes": [{"id": "gs_TqqWfTB97cf3p446fPCt7dmK", "name": "shielded-woodland", "health": 94, "body": [{"x": 6, "y": 8}, {"x": 7, "y": 8}, {"x": 7, "y": 7}, {"x": 8, "y": 7}, {"x": 9, "y": 7}, {"x": 9, "y": 8}, {"x": 10, "y": 8}, {"x": 10, "y": 7}, {"x": 10, "y": 6}, {"x": 10, "y": 5}, {"x": 10, "y": 4}, {"x": 10, "y": 3}, {"x": 10, "y": 2}], "shout": "I like em big... I like em Chunky!"}, {"id": "gs_7wVmbGrvdFpvvpVBR8mGycWb", "name": "csnek", "health": 99, "body": [{"x": 4, "y": 8}, {"x": 4, "y": 7}, {"x": 5, "y": 7}, {"x": 5, "y": 6}, {"x": 6, "y": 6}, {"x": 7, "y": 6}, {"x": 7, "y": 5}, {"x": 6, "y": 5}, {"x": 5, "y": 5}, {"x": 4, "y": 5}, {"x": 3, "y": 5}, {"x": 2, "y": 5}, {"x": 2, "y": 4}, {"x": 2, "y": 3}], "shout": ""}]}, "you": {"id": "gs_TqqWfTB97cf3p446fPCt7dmK", "name": "shielded-woodland", "health": 94, "body": [{"x": 6, "y": 8}, {"x": 7, "y": 8}, {"x": 7, "y": 7}, {"x": 8, "y": 7}, {"x": 9, "y": 7}, {"x": 9, "y": 8}, {"x": 10, "y": 8}, {"x": 10, "y": 7}, {"x": 10, "y": 6}, {"x": 10, "y": 5}, {"x": 10, "y": 4}, {"x": 10, "y": 3}, {"x": 10, "y": 2}], "shout": "I like em big... I like em Chunky!"}}
	move = get_move(data)