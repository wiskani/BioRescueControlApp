"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect, useRouter } from 'next/navigation';

//React imports
import {
    useEffect,
    useCallback,
    useState
}  from 'react';

//Api imports
import {
    DeleteUserApi,
    GetUserById
} from "@/app/libs/users/ApiUsers"

export default function DeleteUser({ params} : { params: { userId: number } }) {
    const { data: session } = useSession();
    const user = session?.user;
    const router = useRouter();
    const [userIdData, setUserIdData] = useState<UsersResponseData | null>(null);

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

    const handleDelete = useCallback( async () => {
        if (user) {
            try {
                await DeleteUserApi({
                    token: user?.token,
                    id: params.userId
                });
                router.push('/users');
            } catch (error) {
                if (error instanceof Error) {
                    console.error(error.message);
                }
            }
        }
    },[user, params.userId, router]);


    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else {
            userData().then((data) => {
                setUserIdData(data);
            });
        }
    }, [session]);


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
                Borrar Usuario
            </h1>
            <p
                className="
                m-6
                text-xl
                text-center
                text-emerald-900
                "
            >
                ¿Está seguro de borrar el usuario?
            </p>
            <p
                className="
                m-6
                text-lg
                text-center
                text-emerald-900
                "
            >
                Nombre: {userIdData?.name}
            </p>
            <p
                className="
                m-6
                text-lg
                text-center
                text-emerald-900
                "
            >
                Apellido: {userIdData?.last_name}
            </p>
            <p
                className="
                m-6
                text-lg
                text-center
                text-emerald-900
                "
            >
                Correo electrónico: {userIdData?.email}
            </p>

            <button
                className='
                text-white
                bg-red-700
                hover:bg-red-800
                focus:ring-4
                focus:outline-none
                focus:ring-red-300
                font-medium
                rounded-lg
                text-sm
                w-full
                sm:w-auto
                px-5
                py-2.5
                text-center
                dark:bg-red-600
                dark:hover:bg-red-700
                dark:focus:ring-red-800
                '
                onClick={handleDelete}
            >
                Borrar
            </button>
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
    );
}

