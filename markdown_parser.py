# 스택 구현 (Stack using Array)
class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.items[-1]

    def size(self):
        return len(self.items)


# 큐 구현 (Queue using Array)
class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            return None
        return self.items[0]

    def size(self):
        return len(self.items)


# 마크다운 파서
class MarkdownParser:
    def __init__(self):
        self.token_queue = Queue()
        self.tag_stack = Stack()

    def tokenize(self, text):
        """문자열을 토큰으로 분리하여 큐에 저장"""
        tokens = []
        i = 0
        while i < len(text):
            if text[i:i+2] == '**':
                tokens.append('**')
                i += 2
            elif text[i] == '*':
                tokens.append('*')
                i += 1
            else:
                # 일반 텍스트 수집
                j = i
                while j < len(text) and text[j:j+2] != '**' and text[j] != '*':
                    j += 1
                tokens.append(text[i:j])
                i = j

        # 큐에 토큰 저장
        for token in tokens:
            self.token_queue.enqueue(token)

    def parse(self, text):
        """마크다운 텍스트를 HTML로 변환"""
        self.token_queue = Queue()
        self.tag_stack = Stack()
        self.tokenize(text)

        result = []

        while not self.token_queue.is_empty():
            token = self.token_queue.dequeue()

            if token == '**':
                result.append(self._handle_bold())
            elif token == '*':
                result.append(self._handle_italic())
            else:
                result.append(token)

        return ''.join(result)

    def _handle_bold(self):
        """** 볼드체 처리 - 스택 사용"""
        if self.tag_stack.is_empty() or self.tag_stack.peek() != 'bold':
            # 볼드 시작
            self.tag_stack.push('bold')
            return '<strong>'
        else:
            # 볼드 끝
            self.tag_stack.pop()
            return '</strong>'

    def _handle_italic(self):
        """* 이태릭체 처리 - 스택 사용"""
        if self.tag_stack.is_empty() or self.tag_stack.peek() != 'italic':
            # 이태릭 시작 (단, **의 일부가 아닌 경우)
            self.tag_stack.push('italic')
            return '<em>'
        else:
            # 이태릭 끝
            self.tag_stack.pop()
            return '</em>'


# 테스트
if __name__ == "__main__":
    parser = MarkdownParser()

    # 테스트 케이스
    test_cases = [
        ("**볼드체**", "볼드체 테스트"),
        ("*이태릭체*", "이태릭체 테스트"),
        ("**볼드**와 *이태릭* 섞기", "혼합 테스트"),
        ("**중첩 *이태릭* 포함**", "중첩 테스트"),
        ("앞 **볼드** 뒤 *이태릭* 끝", "여러 개 테스트"),
    ]

    print("=== 마크다운 파서 테스트 (스택 & 큐 활용) ===\n")

    for markdown, description in test_cases:
        result = parser.parse(markdown)
        print(f"[{description}]")
        print(f"  입력:  {markdown}")
        print(f"  출력:  {result}")
        print()
