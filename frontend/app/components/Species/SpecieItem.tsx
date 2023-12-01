import Image from 'next/image';

const SpecieItem = (props: SpecieItemData) => {
  const imageUrl = props.images && props.images.length > 0 ? `http://localhost:8080${props.images[0].url}` : 'http://localhost:8080/static/images/species/no_imagen.svg';
  return (
    <section className="text-gray-700 body-font overflow-hidden bg-white">
      <div className="container px-5 py-5 mx-auto">
        <div className="mx-auto flex flex-wrap">
            <img alt="specie" className="lg:w-1/2 w-full object-cover object-center rounded border border-gray-200" src={imageUrl}/>
            <div className="w-full mt-6 ">
              <h1 className="text-gray-900 text-xl  title-font font-medium mb-1">Especie: {props.specie_name}</h1>
              <h2 className="text-sm title-font text-gray-500 tracking-widest">Genero: {props.genus_full_name}</h2>
              <div className="flex mt-6 items-center pb-5 border-b-2 border-gray-200 mb-5">
                <div className="flex">
                  <span className="mr-3">Cantidad de Rescates</span>
                  <button className="flex items-center bg-blue-600 text-center text-white justify-center border-2 border-gray-300 rounded-full w-6 h-6 focus:outline-none">{props.total_rescues}</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
  )
}

export default SpecieItem;
