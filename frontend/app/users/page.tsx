"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic'

//React imports
import React, {
    useEffect,
    useState,
    useCallback,
} from "react"

//Api imports
import { GetAllUsers } from '../libs/users/ApiUsers';

//Table imports
import { createColumnHelper } from '@tanstack/react-table';

//Componest imports
import { TableSimple } from '@/app/components/Table/TableSimple';

//Types
interface UsersColumns extends UsersResponseData {
    editar: string;
    borrar:string;
}

export default function Users(){
    const { data: session } = useSession();
    const [users, setUsers] = useState<UsersResponseData[]>([]);
    const router = useRouter();

    const user = session?.user;

    //make columns
    const columnHelper = createColumnHelper<UsersColumns>();

    const columnsUsers = [
        columnHelper.accessor('email', {
                        header: 'Correo electrónico',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('permissions', {
                        header: 'Rol(es)',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('name', {
                        header: 'Nombre',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor('last_name', {
                        header: 'Apellido',
                        footer: info => info.column.id,
                }),
        columnHelper.accessor("id", {
            header: () => <span></span>,
            cell: info => (
                <div className='flex space-x-4'>
                <button
                    className="
                    bg-yellow-500
                    hover:bg-yellow-700
                    text-white
                    font-bold
                    py-2 px-4
                    rounded"
                    onClick={() => {
                        router.push(`/users/edit/${info.getValue()}`)
                    }}
                >
                    Editar
                </button>
                <button
                    className="
                    bg-red-500
                    hover:bg-red-700
                    text-white
                    font-bold
                    py-2 px-4
                    rounded"
                    onClick={() => {
                        router.push(`/users/delete/${info.getValue()}`)
                    }}
                >
                   Borrar 
                </button>

                </div>
            ),
        }

        )
    ]


    const usersData = useCallback(
        async (): Promise<UsersResponseData[]> => {
        if (user) {
            const data = await GetAllUsers({token: user?.token});
            return data;
        }
        else {
            return [];
        }
    }, [user]);

    useEffect(() => {
        if(!session?.user){
            redirect('/');
        }
        else{
            usersData().then((data) => {
                setUsers(data);
            });
        }
    }, [session, usersData]);




    return (
        <div>
            <h1
                className="
                m-6
                text-3xl
                font-bold
                text-center
                text-emerald-900
                "
            >
                Manejo de usuarios
            </h1>

            <div>
                <button
                    className="
                    m-4
                    bg-blue-500
                    hover:bg-blue-700
                    text-white
                    font-bold
                    rounded-full
                    w-8
                    h-8
                    "
                    onClick={() => router.push('/users/create')}
                >
                   + 
                </button>
            </div>

            <TableSimple<UsersResponseData>
                columns={columnsUsers}
                data={users}
            /> 

        </div>
    )

}
