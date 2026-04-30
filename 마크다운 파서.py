import tkinter as tk

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

    def get_items(self):
        return self.items.copy()


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

    def get_items(self):
        return self.items.copy()


class MarkdownParser:
    def tokenize(self, text):
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
                j = i
                while j < len(text) and text[j:j+2] != '**' and text[j] != '*':
                    j += 1
                tokens.append(text[i:j])
                i = j
        return tokens

    def parse(self, text):
        tag_stack = Stack()
        raw_tokens = self.tokenize(text)

        token_queue = Queue()
        for t in raw_tokens:
            token_queue.enqueue(t)

        result = []
        stack_trace = []
        queue_trace = []
        styled_segments = []
        current_text = []
        current_formats = set()

        while not token_queue.is_empty():
            token = token_queue.dequeue()
            queue_trace.append(token_queue.get_items().copy())

            if token == '**':
                if 'bold' in current_formats:
                    if current_text:
                        styled_segments.append((''.join(current_text), current_formats.copy()))
                        current_text = []
                    tag_stack.pop()
                    current_formats.discard('bold')
                    result.append('</bold>')
                    action = "POP bold"
                else:
                    if current_text:
                        styled_segments.append((''.join(current_text), current_formats.copy()))
                        current_text = []
                    tag_stack.push('bold')
                    current_formats.add('bold')
                    result.append('<bold>')
                    action = "PUSH bold"

            elif token == '*':
                if 'italic' in current_formats:
                    if current_text:
                        styled_segments.append((''.join(current_text), current_formats.copy()))
                        current_text = []
                    tag_stack.pop()
                    current_formats.discard('italic')
                    result.append('</italic>')
                    action = "POP italic"
                else:
                    if current_text:
                        styled_segments.append((''.join(current_text), current_formats.copy()))
                        current_text = []
                    tag_stack.push('italic')
                    current_formats.add('italic')
                    result.append('<italic>')
                    action = "PUSH italic"

            else:
                current_text.append(token)
                result.append(token)
                action = "TEXT"

            stack_trace.append({
                'token': token,
                'action': action,
                'stack': tag_stack.get_items().copy()
            })

        if current_text:
            styled_segments.append((''.join(current_text), current_formats.copy()))

        html_result = ''.join(result)
        return html_result, styled_segments, raw_tokens, stack_trace, queue_trace


class RealtimeMarkdownApp:
    def __init__(self, root):
        self.parser = MarkdownParser()
        root.title("Markdown Parser - Stack & Queue")
        root.geometry("950x750")
        root.configure(bg='#1e1e1e')
        self.setup_ui(root)

    def setup_ui(self, root):
        input_frame = tk.Frame(root, bg='#1e1e1e')
        input_frame.pack(fill='x', padx=20, pady=(15, 5))
        tk.Label(input_frame, text="MARKDOWN 입력", font=('Consolas', 11, 'bold'), bg='#1e1e1e', fg='#d4d4d4').pack(anchor='w')

        self.input_text = tk.Text(input_frame, height=3, font=('Consolas', 12), bg='#2d2d2d', fg='#d4d4d4', insertbackground='#d4d4d4')
        self.input_text.pack(fill='x', pady=5)
        self.input_text.bind('<KeyRelease>', self.on_input_change)

        preview_frame = tk.Frame(root, bg='#1e1e1e')
        preview_frame.pack(fill='x', padx=20, pady=10)
        tk.Label(preview_frame, text="미리보기", font=('Consolas', 11, 'bold'), bg='#1e1e1e', fg='#d4d4d4').pack(anchor='w')

        self.preview_text = tk.Text(preview_frame, font=('Malgun Gothic', 13), bg='#2d2d2d', fg='#d4d4d4', relief='solid', bd=1, highlightthickness=0, wrap='word', height=3)
        self.preview_text.pack(fill='x', pady=5, padx=1, ipady=8)
        self.preview_text.tag_config('bold', font=('Malgun Gothic', 13, 'bold'))
        self.preview_text.tag_config('italic', font=('Malgun Gothic', 13, 'italic'))
        self.preview_text.tag_config('bold_italic', font=('Malgun Gothic', 13, 'bold', 'italic'))
        self.preview_text.config(state='disabled')

        html_frame = tk.Frame(root, bg='#1e1e1e')
        html_frame.pack(fill='x', padx=20, pady=5)
        tk.Label(html_frame, text="태그 출력", font=('Consolas', 11, 'bold'), bg='#1e1e1e', fg='#d4d4d4').pack(anchor='w')
        self.html_label = tk.Label(html_frame, text='', font=('Consolas', 11), bg='#2d2d2d', fg='#4ec9b0', anchor='w', justify='left')
        self.html_label.pack(fill='x', pady=5, ipady=8, padx=1)

        viz_frame = tk.Frame(root, bg='#1e1e1e')
        viz_frame.pack(fill='both', expand=True, padx=20, pady=10)

        left_viz = tk.Frame(viz_frame, bg='#1e1e1e')
        left_viz.pack(side='left', fill='both', expand=True, padx=(0, 8))
        tk.Label(left_viz, text="Queue (토큰 대기열)", font=('Consolas', 12, 'bold'), bg='#1e1e1e', fg='#888').pack(anchor='w')
        self.queue_canvas = tk.Canvas(left_viz, bg='#2d2d2d', height=180, highlightthickness=0)
        self.queue_canvas.pack(fill='both', expand=True, pady=5)

        right_viz = tk.Frame(viz_frame, bg='#1e1e1e')
        right_viz.pack(side='right', fill='both', expand=True, padx=(8, 0))
        tk.Label(right_viz, text="Stack (열린 태그)", font=('Consolas', 12, 'bold'), bg='#1e1e1e', fg='#888').pack(anchor='w')
        self.stack_canvas = tk.Canvas(right_viz, bg='#2d2d2d', height=180, highlightthickness=0)
        self.stack_canvas.pack(fill='both', expand=True, pady=5)

    def on_input_change(self, event=None):
        text = self.input_text.get('1.0', 'end-1c')
        if not text.strip():
            self.html_label.config(text='')
            self.preview_text.config(state='normal')
            self.preview_text.delete('1.0', 'end')
            self.preview_text.config(state='disabled')
            self.queue_canvas.delete('all')
            self.stack_canvas.delete('all')
            return

        html_result, styled_segments, raw_tokens, stack_trace, queue_trace = self.parser.parse(text)

        self.html_label.config(text=html_result)
        self.draw_preview(styled_segments)
        self.draw_queue(raw_tokens)
        self.draw_stack(stack_trace[-1]['stack'] if stack_trace else [])

    def draw_preview(self, styled_segments):
        self.preview_text.config(state='normal')
        self.preview_text.delete('1.0', 'end')

        for txt, formats in styled_segments:
            if 'bold' in formats and 'italic' in formats:
                tag = 'bold_italic'
            elif 'bold' in formats:
                tag = 'bold'
            elif 'italic' in formats:
                tag = 'italic'
            else:
                tag = None

            if tag:
                self.preview_text.insert('end', txt, tag)
            else:
                self.preview_text.insert('end', txt)

        self.preview_text.config(state='disabled')

    def draw_queue(self, raw_tokens):
        self.queue_canvas.delete('all')
        if not raw_tokens:
            return

        cw = self.queue_canvas.winfo_width() or 400
        if cw < 100: cw = 400

        bw = min(80, (cw - 30) // max(len(raw_tokens), 1))
        bh, sp = 50, 5
        tw = len(raw_tokens) * (bw + sp) - sp
        sx = (cw - tw) // 2

        for i, token in enumerate(raw_tokens):
            x = sx + i * (bw + sp)
            display = token if token.strip() else ' '
            color = '#42a5f5' if token == '**' else '#ffa726' if token == '*' else '#66bb6a'
            tc = '#fff' if color != '#66bb6a' else '#1e1e1e'

            self.queue_canvas.create_rectangle(x, 15, x + bw, 15 + bh, fill=color, outline='#555', width=1)
            self.queue_canvas.create_text(x + bw//2, 15 + bh//2, text=display[:6], fill=tc, font=('Consolas', 8, 'bold'))

        self.queue_canvas.create_text(cw//2, 160, text=f"{len(raw_tokens)} tokens -> dequeue ->", fill='#666', font=('Consolas', 10))

    def draw_stack(self, stack_items):
        self.stack_canvas.delete('all')
        cw = self.stack_canvas.winfo_width() or 400
        if cw < 100: cw = 400

        if not stack_items:
            self.stack_canvas.create_text(cw//2, 90, text="Empty (모든 태그 닫힘)", fill='#666', font=('Consolas', 10))
            return

        bw = min(140, (cw - 30) // max(len(stack_items), 1))
        bh, sp = 50, 8
        sx = (cw - (len(stack_items) * (bw + sp) - sp)) // 2

        for i, item in enumerate(stack_items):
            x = sx + i * (bw + sp)
            y = 12
            color = '#42a5f5' if item == 'bold' else '#ffa726'
            label = '<bold>' if item == 'bold' else '<italic>'

            self.stack_canvas.create_rectangle(x, y, x + bw, y + bh, fill=color, outline='#555', width=1)
            self.stack_canvas.create_text(x + bw//2, y + bh//2, text=label, fill='#1e1e1e', font=('Consolas', 9, 'bold'))

        self.stack_canvas.create_text(sx + len(stack_items) * (bw + sp), 25, text=" top", fill='#666', font=('Consolas', 10))

if __name__ == "__main__":
    root = tk.Tk()
    app = RealtimeMarkdownApp(root)
    root.mainloop()
