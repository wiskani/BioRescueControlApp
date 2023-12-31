"use client"
//Next imports
import { useSession  } from 'next-auth/react'
import { redirect } from 'next/navigation';


//React imports
import React,{useEffect, useState, useCallback}  from 'react';

//Api imports
import { ApiRescuesSpecie } from "@/app/api/species/route"

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
        
export default function Page({ params} : { params: { specieId: number } }) {
    const { data: session } = useSession();
    const user = session?.user;
    const [rescues, setRescues] = useState<RescuesSpecieData[]>([]);
    const [errorMessage, SetErrorMessage]= useState<string>();


    const rescuesData = useCallback(async (): Promise<RescuesSpecieData[]> => {
            if (user) {
                    try {
                        const data = await ApiRescuesSpecie({ token: user?.token, specie_id: params.specieId });
                        return data;
                    } catch (error) {
                            if (error instanceof Error) {
                                SetErrorMessage(error.message);
                                console.error('Error:', error.message);
                                return [];
                            }
                        return [];
                    }
            }
            else {
                return [];
                }
                }, [user, params.specieId]);

    useEffect(() => {
                        rescuesData().then((data) => {
                                setRescues(data);
                                });
                        }, [session, rescuesData]);


    const renderRescuesData = () => {
            if (rescues.length > 0) {

            return rescues.map((rescue, index) => {
                    if (isFloraRescueSpeciesData(rescue)) {
                        return (
                            <div key={index}>
                                <p>{rescue.epiphyte_number}</p>
                                <p>{rescue.rescue_date.toString()}</p>
                                <p>{rescue.rescue_area_latitude}</p>
                                <p>{rescue.rescue_area_longitude}</p>
                            </div>
                        )
                    }
                    else if (isTransectHerpetoWithSpeciesData(rescue)) {
                        return (
                            <div key={index}>
                                <p>{rescue.number}</p>
                                <p>{rescue.date_in.toString()}</p>
                                <p>{rescue.latitude_in}</p>
                                <p>{rescue.longitude_in}</p>

                            </div>
                        )
                    }

                    else if (isRescueMammalsWithSpecieData(rescue)) {
                        return (
                        <div key={index}>
                                <p>{rescue.cod}</p>
                                <p>{rescue.date.toString()}</p>
                                <p>{rescue.latitude}</p>
                                <p>{rescue.longitude}</p>
                        </div>
                        )
                        }

            })

        }
        else {
                return (
                <div>

                        <p>{errorMessage}</p>
                </div>
                )
        }

    }

        return (
            <div>
            {user 
            ? renderRescuesData()
            : <p>inicia sesión</p>
            }
            </div>
        )
        }

