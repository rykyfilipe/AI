import { Activity, Suspense } from "react";
import type { Message } from "../types";
import MessageCard from "./Message";



function MessagesWindow({messages} : {messages:Message[]}) {
  return (
    <div className="max-w-1/2 min-h-100 h-[80%] overflow-y-auto p-5 no-scrollbar">
        <Suspense fallback={<div className="">No messages </div>}>
            <Activity mode={`${messages.length === 0 ? 'hidden' : 'visible'}`} >
                <div className="">
                    {messages.map((message : Message) => (
                        <MessageCard key={message.id} message={message} />
                    ))}
                </div>
            </Activity>
        </Suspense>
    </div>
  )
}

export default MessagesWindow