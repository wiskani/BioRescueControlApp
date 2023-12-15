"use client"

import * as Dialog from "@radix-ui/react-dialog";
import {Children, type FC, type ReactNode} from "react";
import { useRouter } from "next/navigation";

interface ModalProps {
        children: ReactNode;
        }

const Modal: FC<ModalProps> = ({children}) =>{
        const router = useRouter()

        const handleOpenChange = (open: boolean) => {
                if (!open) {
                        router.back()
                }
        }

        return (
        <Dialog.Root onOpenChange={handleOpenChange}>
                <Dialog.Portal>
                        <Dialog.Overlay className="fixed inset-0 bg-black/70" />
                        <Dialog.DialogContent className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2">
                                {children}
                        </Dialog.DialogContent>
                </Dialog.Portal>
        </Dialog.Root>
        )
}

export default Modal


