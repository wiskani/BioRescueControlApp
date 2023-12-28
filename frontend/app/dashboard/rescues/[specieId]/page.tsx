"use client"
//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';


//React imports
import React,{useEffect, useState, useCallback}  from 'react';

//Api imports
import { RescuesSpecie } from "@/app/api/species/route"

type RescuesSpecieData =
        | FloraRescueSpeciesData
        | TransectHerpetoWithSpeciesData
        | RescueMammalsWithSpecieData 
        
export default function Page({ params} : { params: { specie_id: number } }) {
    const { data: session } = useSession();

    const user = session?.user;
    const [rescues, setRescues] = useState<RescuesSpecieData[]>([]);


    const rescuesData = useCallback(async (): Promise<RescuesSpecieData[]> => {
            if (user) {
                const data = await RescuesSpecie({ token: user.token, specie_id: params.specie_id });
                return data;
            }
            else {
                return [];
                }
                }, [user, params.specie_id]);

    useEffect(() => {
            if(!session?.user){
                redirect("/")
                }
                else{
                        rescuesData().then((data) => {
                                setRescues(data);
                                });
                        }
                        }, [session, rescuesData]);



        return (
            <div>
                <h1>Los Datos son:</h1>

            </div>
        )
        }

