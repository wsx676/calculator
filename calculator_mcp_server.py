import gradio as gr
import math
from typing import Dict, Any, Union

class Calculator:
    def __init__(self):
        # 计算器状态变量
        self.current_input = "0"
        self.operation_stack = []  # 用于存储操作和数字
        self.memory = 0  # 内存功能
        self.result_displayed = False
    
    def add_digit(self, digit):
        # 如果刚显示过结果，则重置
        if self.result_displayed:
            self.current_input = "0"
            self.result_displayed = False
        
        # 添加数字
        if self.current_input == "0":
            self.current_input = digit
        else:
            self.current_input += digit
        
        return self.current_input
    
    def add_decimal(self):
        # 如果刚显示过结果，则重置
        if self.result_displayed:
            self.current_input = "0"
            self.result_displayed = False
        
        # 添加小数点
        if "." not in self.current_input:
            self.current_input += "."
        
        return self.current_input
    
    def add_operation(self, operation):
        # 如果有当前输入，将其添加到操作栈
        if self.current_input != "0" or len(self.operation_stack) > 0:
            # 如果上一个是操作符，则替换它
            if len(self.operation_stack) > 0 and self.operation_stack[-1] in ["+", "-", "*", "/"]:
                self.operation_stack[-1] = operation
            else:
                # 添加当前输入和操作符到栈
                self.operation_stack.append(self.current_input)
                self.operation_stack.append(operation)
            
            # 重置当前输入
            self.current_input = "0"
            self.result_displayed = False
            
            return {"current_input": self.current_input, "operation_stack": self.operation_stack}
        return {"current_input": self.current_input, "operation_stack": self.operation_stack}
    
    def calculate(self):
        # 如果有当前输入，将其添加到操作栈
        if self.current_input != "0" or len(self.operation_stack) == 0:
            self.operation_stack.append(self.current_input)
        
        # 计算表达式
        try:
            expression = "".join(self.operation_stack)
            result = eval(expression)
            
            # 格式化结果
            if result == int(result):
                result = int(result)
            
            # 更新显示
            self.current_input = str(result)
            self.operation_stack = []
            self.result_displayed = True
            
            return {"result": self.current_input, "success": True}
        except Exception as e:
            self.current_input = "错误"
            self.operation_stack = []
            return {"result": "错误", "error": str(e), "success": False}
    
    def clear(self):
        # 清除所有
        self.current_input = "0"
        self.operation_stack = []
        self.result_displayed = False
        return {"current_input": self.current_input, "operation_stack": self.operation_stack}
    
    def clear_entry(self):
        # 只清除当前输入
        self.current_input = "0"
        self.result_displayed = False
        return {"current_input": self.current_input}
    
    def backspace(self):
        # 退格
        if self.result_displayed:
            return {"current_input": self.current_input}
        
        if len(self.current_input) > 1:
            self.current_input = self.current_input[:-1]
        else:
            self.current_input = "0"
        
        return {"current_input": self.current_input}
    
    def negate(self):
        # 正负号切换
        if self.current_input != "0":
            if self.current_input[0] == "-":
                self.current_input = self.current_input[1:]
            else:
                self.current_input = "-" + self.current_input
            
            return {"current_input": self.current_input}
        return {"current_input": self.current_input}
    
    def calculate_sqrt(self):
        # 计算平方根
        try:
            value = float(self.current_input)
            if value < 0:
                raise ValueError("不能对负数开平方根")
            
            result = math.sqrt(value)
            
            # 格式化结果
            if result == int(result):
                result = int(result)
            
            self.current_input = str(result)
            self.result_displayed = True
            return {"result": self.current_input, "success": True}
        except Exception as e:
            self.current_input = "错误"
            return {"result": "错误", "error": str(e), "success": False}
    
    def calculate_square(self):
        # 计算平方
        try:
            value = float(self.current_input)
            result = value ** 2
            
            # 格式化结果
            if result == int(result):
                result = int(result)
            
            self.current_input = str(result)
            self.result_displayed = True
            return {"result": self.current_input, "success": True}
        except Exception as e:
            self.current_input = "错误"
            return {"result": "错误", "error": str(e), "success": False}
    
    def calculate_reciprocal(self):
        # 计算倒数
        try:
            value = float(self.current_input)
            if value == 0:
                raise ValueError("不能除以零")
            
            result = 1 / value
            
            # 格式化结果
            if result == int(result):
                result = int(result)
            
            self.current_input = str(result)
            self.result_displayed = True
            return {"result": self.current_input, "success": True}
        except Exception as e:
            self.current_input = "错误"
            return {"result": "错误", "error": str(e), "success": False}
    
    def calculate_percentage(self):
        # 计算百分比
        try:
            value = float(self.current_input)
            result = value / 100
            
            # 格式化结果
            if result == int(result):
                result = int(result)
            
            self.current_input = str(result)
            self.result_displayed = True
            return {"result": self.current_input, "success": True}
        except Exception as e:
            self.current_input = "错误"
            return {"result": "错误", "error": str(e), "success": False}
    
    def memory_clear(self):
        # 清除内存
        self.memory = 0
        return {"memory": self.memory}
    
    def memory_recall(self):
        # 调用内存
        self.current_input = str(self.memory)
        return {"current_input": self.current_input, "memory": self.memory}
    
    def memory_add(self):
        # 内存加
        try:
            value = float(self.current_input)
            self.memory += value
            return {"memory": self.memory, "success": True}
        except Exception as e:
            return {"memory": self.memory, "error": str(e), "success": False}
    
    def memory_subtract(self):
        # 内存减
        try:
            value = float(self.current_input)
            self.memory -= value
            return {"memory": self.memory, "success": True}
        except Exception as e:
            return {"memory": self.memory, "error": str(e), "success": False}
    
    def memory_store(self):
        # 存储到内存
        try:
            self.memory = float(self.current_input)
            return {"memory": self.memory, "success": True}
        except Exception as e:
            return {"memory": self.memory, "error": str(e), "success": False}
    
    def get_state(self):
        # 获取当前计算器状态
        return {
            "current_input": self.current_input,
            "operation_stack": self.operation_stack,
            "memory": self.memory,
            "result_displayed": self.result_displayed
        }

# 创建MCP服务器（使用Gradio）
def create_calculator_server():
    calculator = Calculator()
    
    # 定义Gradio接口函数
    def add_digit(digit):
        result = calculator.add_digit(digit)
        return result, str(calculator.operation_stack)
    
    def add_decimal():
        result = calculator.add_decimal()
        return result, str(calculator.operation_stack)
    
    def add_operation(operation):
        result = calculator.add_operation(operation)
        return result["current_input"], str(result["operation_stack"])
    
    def calculate():
        result = calculator.calculate()
        if result["success"]:
            return result["result"], str(calculator.operation_stack)
        else:
            return "错误", str(calculator.operation_stack)
    
    def clear():
        result = calculator.clear()
        return result["current_input"], str(result["operation_stack"])
    
    def clear_entry():
        result = calculator.clear_entry()
        return result["current_input"], str(calculator.operation_stack)
    
    def backspace():
        result = calculator.backspace()
        return result["current_input"], str(calculator.operation_stack)
    
    def negate():
        result = calculator.negate()
        return result["current_input"], str(calculator.operation_stack)
    
    def calculate_sqrt():
        result = calculator.calculate_sqrt()
        if result["success"]:
            return result["result"], str(calculator.operation_stack)
        else:
            return "错误", str(calculator.operation_stack)
    
    def calculate_square():
        result = calculator.calculate_square()
        if result["success"]:
            return result["result"], str(calculator.operation_stack)
        else:
            return "错误", str(calculator.operation_stack)
    
    def calculate_reciprocal():
        result = calculator.calculate_reciprocal()
        if result["success"]:
            return result["result"], str(calculator.operation_stack)
        else:
            return "错误", str(calculator.operation_stack)
    
    def calculate_percentage():
        result = calculator.calculate_percentage()
        if result["success"]:
            return result["result"], str(calculator.operation_stack)
        else:
            return "错误", str(calculator.operation_stack)
    
    def memory_clear():
        calculator.memory_clear()
        return calculator.current_input, str(calculator.operation_stack)
    
    def memory_recall():
        result = calculator.memory_recall()
        return result["current_input"], str(calculator.operation_stack)
    
    def memory_add():
        calculator.memory_add()
        return calculator.current_input, str(calculator.operation_stack)
    
    def memory_subtract():
        calculator.memory_subtract()
        return calculator.current_input, str(calculator.operation_stack)
    
    def memory_store():
        calculator.memory_store()
        return calculator.current_input, str(calculator.operation_stack)
    
    def get_calculator_state():
        return str(calculator.get_state())
    
    # 创建Gradio界面
    with gr.Blocks(title="计算器 MCP 服务器") as demo:
        gr.Markdown("# 计算器 MCP 服务器")
        
        with gr.Row():
            display = gr.Textbox(value="0", label="显示")
            stack_display = gr.Textbox(value="[]", label="操作栈")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 数字")
                with gr.Row():
                    btn7 = gr.Button("7")
                    btn8 = gr.Button("8")
                    btn9 = gr.Button("9")
                with gr.Row():
                    btn4 = gr.Button("4")
                    btn5 = gr.Button("5")
                    btn6 = gr.Button("6")
                with gr.Row():
                    btn1 = gr.Button("1")
                    btn2 = gr.Button("2")
                    btn3 = gr.Button("3")
                with gr.Row():
                    btn0 = gr.Button("0")
                    btn_decimal = gr.Button(".")
                    btn_equals = gr.Button("=")
            
            with gr.Column():
                gr.Markdown("### 操作")
                with gr.Row():
                    btn_add = gr.Button("+")
                    btn_subtract = gr.Button("-")
                with gr.Row():
                    btn_multiply = gr.Button("*")
                    btn_divide = gr.Button("/")
                with gr.Row():
                    btn_clear = gr.Button("C")
                    btn_clear_entry = gr.Button("CE")
                with gr.Row():
                    btn_backspace = gr.Button("⌫")
                    btn_negate = gr.Button("+/-")
            
            with gr.Column():
                gr.Markdown("### 高级功能")
                with gr.Row():
                    btn_sqrt = gr.Button("√")
                    btn_square = gr.Button("x²")
                with gr.Row():
                    btn_reciprocal = gr.Button("1/x")
                    btn_percentage = gr.Button("%")
                with gr.Row():
                    btn_mc = gr.Button("MC")
                    btn_mr = gr.Button("MR")
                with gr.Row():
                    btn_mplus = gr.Button("M+")
                    btn_mminus = gr.Button("M-")
                    btn_ms = gr.Button("MS")
        
        with gr.Row():
            state_btn = gr.Button("获取计算器状态")
            state_display = gr.Textbox(label="计算器状态")
        
        # 绑定事件
        btn0.click(fn=lambda: add_digit("0"), outputs=[display, stack_display])
        btn1.click(fn=lambda: add_digit("1"), outputs=[display, stack_display])
        btn2.click(fn=lambda: add_digit("2"), outputs=[display, stack_display])
        btn3.click(fn=lambda: add_digit("3"), outputs=[display, stack_display])
        btn4.click(fn=lambda: add_digit("4"), outputs=[display, stack_display])
        btn5.click(fn=lambda: add_digit("5"), outputs=[display, stack_display])
        btn6.click(fn=lambda: add_digit("6"), outputs=[display, stack_display])
        btn7.click(fn=lambda: add_digit("7"), outputs=[display, stack_display])
        btn8.click(fn=lambda: add_digit("8"), outputs=[display, stack_display])
        btn9.click(fn=lambda: add_digit("9"), outputs=[display, stack_display])
        
        btn_decimal.click(fn=add_decimal, outputs=[display, stack_display])
        btn_equals.click(fn=calculate, outputs=[display, stack_display])
        
        btn_add.click(fn=lambda: add_operation("+"), outputs=[display, stack_display])
        btn_subtract.click(fn=lambda: add_operation("-"), outputs=[display, stack_display])
        btn_multiply.click(fn=lambda: add_operation("*"), outputs=[display, stack_display])
        btn_divide.click(fn=lambda: add_operation("/"), outputs=[display, stack_display])
        
        btn_clear.click(fn=clear, outputs=[display, stack_display])
        btn_clear_entry.click(fn=clear_entry, outputs=[display, stack_display])
        btn_backspace.click(fn=backspace, outputs=[display, stack_display])
        btn_negate.click(fn=negate, outputs=[display, stack_display])
        
        btn_sqrt.click(fn=calculate_sqrt, outputs=[display, stack_display])
        btn_square.click(fn=calculate_square, outputs=[display, stack_display])
        btn_reciprocal.click(fn=calculate_reciprocal, outputs=[display, stack_display])
        btn_percentage.click(fn=calculate_percentage, outputs=[display, stack_display])
        
        btn_mc.click(fn=memory_clear, outputs=[display, stack_display])
        btn_mr.click(fn=memory_recall, outputs=[display, stack_display])
        btn_mplus.click(fn=memory_add, outputs=[display, stack_display])
        btn_mminus.click(fn=memory_subtract, outputs=[display, stack_display])
        btn_ms.click(fn=memory_store, outputs=[display, stack_display])
        
        state_btn.click(fn=get_calculator_state, outputs=state_display)
    
    return demo

if __name__ == "__main__":
    # 创建并启动MCP服务器
    demo = create_calculator_server()
    demo.launch(mcp_server = True)