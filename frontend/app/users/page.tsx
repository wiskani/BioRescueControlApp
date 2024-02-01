"use client"

//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic'

//React imports
import React, { useEffect, useState, useCallback } from "react"

//Api imports
import { GetAllUsers } from '../libs/users/ApiUsers';

export default function Users(){
    const { data: session } = useSession();
    const [users, setUsers] = useState<UsersResponseData[]>([]);

    const user = session?.user;

    const usersData = useCallback(async (): Promise<UsersResponseData[]> => {
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

        </div>
    )

}
