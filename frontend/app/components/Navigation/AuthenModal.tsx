"use client";

import React, { useState } from "react";

interface UserModalComponentProps {
    modal_id: string;
    title: string;
    text: string;
    triggerAccept?: null | ((a: any) => void);
    triggerValue?: any | null;
    triggerString?: string | null;
}

import VerbaButton from "./VerbaButton";
import { set } from "date-fns";

const AuthenModal: React.FC<UserModalComponentProps> = ({
    title,
    modal_id,
    text,
    triggerAccept,
    triggerString,
    triggerValue,
}) => {
    const [password, setPassword] = useState("");

    return (
        <dialog id={modal_id} className="modal">
            <div className="modal-box flex flex-col gap-4">
                <h3 className="font-bold text-lg">{title}</h3>
                <p className="whitespace-pre-wrap">{text}</p>

                <label className="input flex items-center w-full bg-bg-verba">
                    <input
                        type="password"
                        className="grow w-full"
                        placeholder="Enter your password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />
                </label>

                <div className="modal-action">
                    <form method="dialog" className="flex gap-2 ml-auto">
                        {triggerAccept && triggerString && (
                            <VerbaButton
                                type="submit"
                                title={triggerString}
                                onClick={() => {
                                    if (password === "the-infitech") {
                                        triggerAccept(triggerValue);
                                    } else {
                                        alert("Incorrect password");
                                    }
                                    setPassword("");
                                }}
                            />
                        )}
                        <VerbaButton
                            type="submit"
                            title="Cancel"
                            selected_color="bg-warning-verba"
                            selected={true}
                        />
                    </form>
                </div>
            </div>
        </dialog>

    );
};

export default AuthenModal;
