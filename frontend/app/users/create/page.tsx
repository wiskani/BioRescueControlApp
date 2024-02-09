"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect, useRouter } from 'next/navigation';

//React imports
import React, {
    useEffect,
    useState,
    useCallback,
    FormEvent
} from "react"

//Api imports
import { PostUser } from '@/app/libs/users/ApiUsers';

export default function CreateUser(){
    const { data: session } = useSession();
    const router = useRouter();

    const user = session?.user;

    async function onSubmit(event: FormEvent<HTMLFormElement>){
        event.preventDefault()
        const formData = new FormData(event.currentTarget)

        const userPermisions = () => { 
            return [formData.get('permissions') as string]
        }

        const dataUser: UsersCreateData  = {
            email: formData.get('email') as string,
            name: formData.get('name') as string,
            last_name: formData.get('last_name') as string,
            permissions: userPermisions(),
            hashed_password: formData.get('password') as string
        }

        if (!user){
            throw new Error('No user found')
        }

        const response = await PostUser({
            token: user?.token,
            dataUser
        })

        if(response){
            router.push('/users');
        } else {
            throw new Error('Error creating user')
        }

    }

    useEffect(() => {
        if(!session?.user){
            redirect('/');
        }
    }, [session]);

    return (
    <div>
        <h1>Create User</h1>
        <div>
                <form
                    onSubmit={onSubmit}
                    className='max-w-sm mx-auto'
                >
                    <div className='mb-5'>
                        <label
                            className='
                            block
                            mb-2
                            text-sm
                            font-medium
                            text-gray-900
                            dark:text-white
                            '
                        >
                            Correo electrónico:
                            <input
                                type="email"
                                name="email"
                                className='
                                bg-gray-50
                                border
                                border-gray-300
                                text-gray-900
                                text-sm
                                rounded-lg
                                focus:ring-blue-500
                                focus:border-blue-500
                                block
                                w-full
                                p-2.5
                                dark:bg-gray-700
                                dark:border-gray-600
                                dark:placeholder-gray-400
                                dark:text-white
                                dark:focus:ring-blue-500
                                dark:focus:border-blue-500
                                '
                            />
                        </label>
                    </div>
                    <div className='mb-5'> 
                        <label
                            className='
                            block
                            mb-2
                            text-sm
                            font-medium
                            text-gray-900
                            dark:text-white
                            '
                        >
                            Rol(es):
                            <select
                                name="permissions"
                                className='
                                bg-gray-50
                                border
                                border-gray-300
                                text-gray-900
                                text-sm
                                rounded-lg
                                focus:ring-blue-500
                                focus:border-blue-500
                                block
                                w-full
                                p-2.5
                                dark:bg-gray-700
                                dark:border-gray-600
                                dark:placeholder-gray-400
                                dark:text-white
                                dark:focus:ring-blue-500
                                dark:focus:border-blue-500
                                '
                            >
                                <option value="admin">Administrador</option>
                                <option value="user">Usuario</option>
                            </select>
                        </label>
                    </div>
                    <div className='mb-5'>
                        <label
                            className='
                            block
                            mb-2
                            text-sm
                            font-medium
                            text-gray-900
                            dark:text-white
                            '
                        >
                            Nombre:
                            <input
                                type="text"
                                name="name"
                                className='
                                bg-gray-50
                                border
                                border-gray-300
                                text-gray-900
                                text-sm
                                rounded-lg
                                focus:ring-blue-500
                                focus:border-blue-500
                                block
                                w-full
                                p-2.5
                                dark:bg-gray-700
                                dark:border-gray-600
                                dark:placeholder-gray-400
                                dark:text-white
                                dark:focus:ring-blue-500
                                dark:focus:border-blue-500
                                '
                            />
                        </label>
                    </div>
                    <div>
                        <label
                            className='
                            block
                            mb-2
                            text-sm
                            font-medium
                            text-gray-900
                            dark:text-white
                            '
                        >
                            Apellido:
                            <input
                                type="text"
                                name="last_name"
                                className='
                                bg-gray-50
                                border
                                border-gray-300
                                text-gray-900
                                text-sm
                                rounded-lg
                                focus:ring-blue-500
                                focus:border-blue-500
                                block
                                w-full
                                p-2.5
                                dark:bg-gray-700
                                dark:border-gray-600
                                dark:placeholder-gray-400
                                dark:text-white
                                dark:focus:ring-blue-500
                                dark:focus:border-blue-500
                                '
                            />
                        </label>
                    </div>
                    <div>
                        <label
                            className='
                            block
                            mb-2
                            text-sm
                            font-medium
                            text-gray-900
                            dark:text-white
                            '
                        >
                            Contraseña:
                            <input
                                type="password"
                                name="password"
                                className='
                                bg-gray-50
                                border
                                border-gray-300
                                text-gray-900
                                text-sm
                                rounded-lg
                                focus:ring-blue-500
                                focus:border-blue-500
                                block
                                w-full
                                p-2.5
                                dark:bg-gray-700
                                dark:border-gray-600
                                dark:placeholder-gray-400
                                dark:text-white
                                dark:focus:ring-blue-500
                                dark:focus:border-blue-500
                                '
                            />
                        </label>
                    </div>
                    <div className='flex space-x-4'>
                        <button
                            type="submit"
                            className='
                            text-white
                            bg-blue-700
                            hover:bg-blue-800
                            focus:ring-4
                            focus:outline-none
                            focus:ring-blue-300
                            font-medium
                            rounded-lg
                            text-sm
                            w-full
                            sm:w-auto
                            px-5
                            py-2.5
                            text-center
                            dark:bg-blue-600
                            dark:hover:bg-blue-700
                            dark:focus:ring-blue-800
                            '
                        >
                            Crear
                        </button>
                    </div>
                </form>
        </div>
    </div>
    )

}
