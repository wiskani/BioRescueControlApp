"use client"

import { useSession  } from 'next-auth/react'
import React,{useEffect, useState}  from 'react';
import { redirect } from 'next/navigation';
import dynamic from 'next/dynamic';
import { ApiRescueFlora } from "../api/rescue_flora/route";
import SpecieItem from '../components/Species/SpecieItem';

const MyMap =  dynamic(() => import('../components/Map/Map'), {ssr: false});

export default function Dashboard() {
    const { data: session } = useSession();
    const [centers, setCenters] = useState([])
    const user = session?.user;
    const rescueDataFlora =async ()=>{
      if (user){
       const data= await ApiRescueFlora({token: user?.token})
       return data.map((item:FloraRescueData)=>[item.rescue_area_latitude, item.rescue_area_longitude] )
      }
      else{
        return []
      }
    }
    useEffect(() => {
        if (!session?.user) {
            redirect('/')
        }
        else{
            rescueDataFlora().then((data)=>{
                setCenters(data)
            })

        }
    }, [session])
        return (
            <div>
                <div className="flex flex-col  h-96 2xl:mb-52 xl:mb-52 lg:mb-40 md:flex-row md:mb-0 sm:mb-0 justify-center">
                    <div className="h-full p-0 z-50 md:w-1/2 p-4 md:h-[16rem] sd:h-[6rem]">
                        <MyMap centers={centers}/>
                    </div>
                    <div className='md:w-1/2 p-4'>
                        <h1> Hola datos </h1>
                    </div>
                </div>
                    <SpecieItem />

            </div>
        )

}
