import litellm
import json
import os

class Tool:
    def __init__(self, name, description, func, parameters):
        self.name = name
        self.description = description
        self.func = func
        self.parameters = parameters
        self.schema = self._generate_schema()
        
    def _generate_schema(self):
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

class Agent:
    def __init__(self, tools=None):
        self.conversation = list()
        self.tools = tools
        
    def _handle_tool_calls(self, message):
        self.conversation.append(message.model_dump())
        
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            
            for tool in self.tools:
                if tool_name == tool.name:
                    try:
                        result = tool.func(**tool_args) 
                        result = str(result)
                        break
                    except Exception as e:
                        result = f"Erro ao executar {tool_name}: {str(e)}"
                        print(e)
                        break
            else:
                result = f"Ferramenta {tool_name} não encontrada"
                
            self.conversation.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
         
        #print(self.conversation)
        response = litellm.completion(
            model="gpt-4.1",
            messages=self.conversation
        )
        
        response_message = response.choices[0].message.content
        self.conversation.append({
            "role": "assistant",
            "content": response_message
        })
        print(f"Agente: {response_message}")

    
    def run(self):
        print("Agente iniciado")
        
        while True:
            user_input = input("Voce: ")
            
            if user_input.lower() == "sair":
                print("Tchau")
                break
            
            user_msg = {"role": "user", "content": user_input}
            
            self.conversation.append(user_msg)
            
            tools_schemas = [tool.schema for tool in self.tools]
            
            response = litellm.completion(
                model="gpt-4.1",
                messages = self.conversation,
                tools=tools_schemas
            )
            
            assistant_message = response.choices[0].message

            
            
            if assistant_message.tool_calls:
                self._handle_tool_calls(assistant_message)
            else:
                self.conversation.append({"role": "assistant", "content": assistant_message})
                print(f"Agente: {assistant_message}")

def list_files():
    files = os.listdir(".")
    return "\n".join(files)

def read_file(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        return f.read()
    
def write_file(file_path, content):
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(content)
        return f"Conteúdo {content} escrito para o arquivo"
    
if __name__ == "__main__":
    list_files_tool = Tool(name="list_files",
                           description="Lista os arquivos disponíveis no diretório atual",
                           func=list_files,
                           parameters={
                               "type": "object",
                               "properties": {},
                               "required": []
                           })
    read_file_tool = Tool(name="read_file",
                           description="Lê o arquivo especificado por file_path",
                           func=read_file,
                           parameters={
                               "type": "object",
                               "properties": {
                                    "file_path": {
                                        "type": "string",
                                        "description": "Caminho para o arquivo a ser lido"
                                    }   
                                },
                               "required": ["file_path"]
                           })
    write_file_tool = Tool(name="write_file",
                        description="Trunca e escreve para o arquivo especificado por file_path",
                        func=write_file,
                        parameters={
                            "type": "object",
                            "properties": {
                                "file_path": {
                                    "type": "string",
                                    "description": "Caminho para o arquivo a ser lido"
                                },
                                "content": {
                                    "type": "string",
                                    "description": "Conteúdo para escrever dentro do arquivo"
                                }   
                            },
                            "required": ["file_path", "content"]
                        })
    
    
    
    agent = Agent(tools=[list_files_tool, read_file_tool, write_file_tool])
    agent.run()