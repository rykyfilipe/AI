import { SendHorizonal } from "lucide-react";
import { useState } from "react";

interface Props{
    update : (message: string) => void;
}

function InputBar({update} :Props) {

    const [message, setMessage] = useState<string>("");

  return (
    <div className="w-full bg-white flex justify-center">
    <div className="max-w-[70%] min-w-[40%]  p-3">
        <form className="w-full flex items-center justify-between"
        onSubmit={(e) => {
            e.preventDefault();

            if(message.trim() === "") return;

            update(message);
            setMessage("");
            }}>
            <input type="text" placeholder="Send a message" value={message} onChange={(e) => setMessage(e.currentTarget.value)}
                className="w-full focus:outline-none"
            />
            <button type="submit" className="hover:cursor-pointer">
                <SendHorizonal className="text-black/80"/>
            </button>
        </form>
        </div>
    </div>
  )
}

export default InputBar