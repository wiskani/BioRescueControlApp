"use client"

import { useSession  } from 'next-auth/react'
import React,{useEffect}  from 'react';
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic';

const MyMap =  dynamic(() => import('../components/Map/Map'), {ssr: false});

export default function Dashboard() {
    const { data: session } = useSession();
    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
    }, [session])
        return (
            <div className="flex flex-col  h-96 md:flex-row justify-center">
                <div className="h-full p-0 z-50 md:w-1/2 p-4 md:h-[16rem] sd:h-[6rem]">
                    <MyMap/>
                </div>
                <div className='md:w-1/2 p-4'>
                    <h1> Hola datos </h1>
                </div>
            </div>
        )

}
