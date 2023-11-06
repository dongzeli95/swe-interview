```python


class Solution(object):
    visited = set()
    vector = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    def dfs(self, x, y, dir, robot):
        robot.clean()
        self.visited.add((x, y))
        for i in range(4):
            idx = (dir+i) % 4
            tempX = x + self.vector[idx][0]
            tempY = y + self.vector[idx][1]

            if not (tempX, tempY) in self.visited and robot.move() == True:
                self.dfs(tempX, tempY, idx, robot)
                self.move_back(robot)

            robot.turnRight()
    
    def move_back(self, robot):
        robot.turnLeft()
        robot.turnLeft()
        robot.move()
        robot.turnLeft()
        robot.turnLeft()

    def cleanRoom(self, robot):
        self.visited = set()
        self.dfs(0, 0, 0, robot)```
