"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect, useRouter } from 'next/navigation';

//React imports
import {
    useEffect,
    useCallback,
    useState,
    FormEvent
}  from 'react';

//Api imports
import {
    GetUserById,
    UpdateUserApi
} from "@/app/libs/users/ApiUsers"

export default function UpdateUser({params} : { params: { userId: number}}) {
    const { data: session } = useSession();
    const user = session?.user;
    const router = useRouter();
    const [userIdData, setUserIdData] = useState<UsersResponseData | null>(null);

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

        const response = await UpdateUserApi({
            token: user?.token,
            id: params.userId,
            dataUser
        })

        if(response){
            router.push('/users');
        } else {
            throw new Error('Error update user')
        }

    }

    const userData = useCallback(
        async (): Promise<UsersResponseData>=> {
            if (user) {
                try {
                    const data = await GetUserById({
                        token: user?.token,
                        id: params.userId
                    });
                    return data;
                } catch (error) {
                    if (error instanceof Error) {
                        console.error(error.message);
                        throw error;
                    }
                    throw error;
                }

            }
            throw new Error('User not found');
        }, [user, params.userId]);

    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else {
            userData().then((data) => {
                setUserIdData(data);
            });
        }
    }, [session, userData]);


    return (
        <div
            className="
            flex
            flex-col
            justify-center
            items-center
            "
        >
            <h1
                className="
                m-6
                text-xl
                font-bold
                text-center
                text-emerald-900
                "
            >
                Editar usuario
            </h1>
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
                                defaultValue={userIdData?.email}
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
                                value={userIdData?.permissions}
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
                                defaultValue={userIdData?.name}
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
                                defaultValue={userIdData?.last_name}
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
                            Modificar 
                        </button>
                    </div>
                </form>
        </div>
            <button
                className='group'
                onClick={() => router.push('/users')}
            >
                <svg
                    className="
                    m-6
                    w-8 h-8
                    text-emerald-700
                    group-hover:text-emerald-900
                    dark:text-white
                    "
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke="currentColor"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth="2"
                        d="M3 9h13a5 5 0 0 1 0 10H7M3 9l4-4M3 9l4 4"/>
                </svg>

            </button>
    </div>
    )


}
