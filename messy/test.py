class Queue:
    def __init__(self):
        self._queue = []
        self.print_info = []

    def operation(self, type):
        if type.startswith('PUSH'):
            self.push(type)
        elif type == 'TOP':
            self.top()
        elif type == 'POP':
            self.pop()
        elif type == 'SIZE':
            self.size()
        elif type == 'CLEAR':
            self.clear()

    def push(self, type):
        num = type.split(' ')[1]
        self._queue.append(num)

    def top(self):
        if not self._queue:
            # print(-1)
            self.print_info.append("-1")
        else:
            # print(self._queue[0])
            self.print_info.append(self._queue[0])

    def pop(self):
        if not self._queue:
            # print(-1)
            self.print_info.append("-1")
        else:
            # print(self._queue[0])
            # self.print_info.append(self._queue[0])
            self._queue = self._queue[1:]
            self._queue.pop()

    def size(self):
        # print(len(self._queue))
        self.print_info.append(str(len(self._queue)))

    def clear(self):
        self._queue.clear()

    def run(self):
        grourp = int(input())
        for _ in range(grourp):
            op_nums = int(input())
            for _ in range(op_nums):
                operation_type = input()
                self.operation(operation_type)
        # print(self.print_info)
        for s in self.print_info:
            print(str(s))

Queue().run()