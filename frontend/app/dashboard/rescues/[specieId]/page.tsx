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

//predicados fuctions
function isFloraRescueSpeciesData(data: RescuesSpecieData): data is FloraRescueSpeciesData {
    return  data && "epiphyte_number" in data;
}

function isTransectHerpetoWithSpeciesData(data: RescuesSpecieData): data is TransectHerpetoWithSpeciesData {
    return  data && "number" in data;
}

function isRescueMammalsWithSpecieData(data: RescuesSpecieData): data is RescueMammalsWithSpecieData {
    return  data && "cod" in data;
}
        
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


    const renderRescuesData = () => {
            return rescues.map((rescue, index) => {
                    if (isFloraRescueSpeciesData(rescue)) {
                        return (
                            <div>
                                <p>{rescue.epiphyte_number}</p>
                                <p>{rescue.rescue_date.toString()}</p>
                                <p>{rescue.rescue_area_latitude}</p>
                                <p>{rescue.rescue_area_longitude}</p>
                            </div>
                        )
                    }
                    if (isTransectHerpetoWithSpeciesData(rescue)) {
                        return (
                            <div>
                                <p>{rescue.number}</p>
                                <p>{rescue.date_in.toString()}</p>
                                <p>{rescue.latitude_in}</p>
                                <p>{rescue.longitude_in}</p>

                            </div>
                        )
                    }
            })

        return (
            <div>
                <h1>Los Datos son:</h1>
            </div>
        )
        }

