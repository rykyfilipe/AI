import { Bot } from "lucide-react"
import type { Message } from "../types"

function MessageCard({message}:{message: Message}) {
  return (
    <div className={`w-full flex ${message.owner === 'AI' ? '' : 'justify-end'} mb-5`}>
        <div className="max-w-[70%] h-auto bg-white p-2 rounded-xl flex items-center gap-3">
            <div className={`${message.owner === 'AI' ? 'block' : 'hidden'} `}>
                <Bot className="bg-blue-900 text-white h-7 w-7 p-0.5 rounded-full"/>
            </div>

            <p className="max-w-full break-words whitespace-pre-wrap">{message.value}</p>
        </div>
    </div>
  )
}

export default MessageCard