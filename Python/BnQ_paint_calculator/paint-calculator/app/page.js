"use client";
import Image from "next/image";
import { useState, useMemo } from "react";
import { Select, SelectSection, SelectItem } from "@nextui-org/select";
import { Accordion, AccordionItem } from "@nextui-org/accordion";
import { Input } from "@nextui-org/input";
import { Checkbox } from "@nextui-org/checkbox";
import { Button } from "@nextui-org/button";
import AccordionWall from "./components/accordianWall";
import { callAPI } from "./actions";
import axios from "axios";

// async function getData(wallState) {
//   console.log("Calling API");
//   try {
//     // Fetch data from external API
//     const res = await fetch("http://localhost:5000/calculate_paint", {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify({ nosWalls: wallState }),
//     });

//     if (!response.ok) {
//       throw new Error(`HTTP error! Status: ${response.status}`);
//     }

//     const repo = await res.json();
//     // Pass data to the page via props
//     return repo;
//   } catch (error) {
//     console.error("Error calculating paint:", error);
//   }
// }

export default function Home() {
  let maxWalls = 10;
  let minWalls = 1;
  let maxCoats = 3;
  let minCoats = 1;
  let brands = [
    { label: "Cheap", value: "cheap", description: "5 sqm/L" },
    { label: "Medium", value: "medium", description: "10 sqm/L" },
    { label: "Expensive", value: "expensive", description: "15 sqm/L" },
  ];

  const [wallState, setWallState] = useState(1);
  const [coatState, setCoatState] = useState(1);
  const [measure, setMeasure] = useState("0");
  const [brand, setBrand] = useState(new Set([]));
  const [data, setData] = useState("");

  const disabled_keys = [];
  for (let i = wallState + 1; i <= 10; i++) {
    disabled_keys.push(String(i));
  }

  const addWall = () => {
    if (wallState < maxWalls) {
      setWallState(wallState + 1);
    }
  };

  const subWall = () => {
    if (wallState > minWalls) {
      setWallState(wallState - 1);
    }
  };

  const addCoat = () => {
    if (coatState < maxCoats) {
      setCoatState(coatState + 1);
    }
  };

  const subCoat = () => {
    if (coatState > minCoats) {
      setCoatState(coatState - 1);
    }
  };

  const handleAPI = (wallState) => {
    axios
      .post("http://localhost:5000/calculate_paint", { input: wallState })
      .then((response) => {
        console.log("YUH");
        setData(response.data.output);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // const callAPI = async () => {
  //   const endpointData = await getData(wallState);
  //   setData(endpointData);
  // };

  return (
    <main className="flex min-h-screen max-w-4xl flex-row justify-center mb-40 mt-16 mx-auto w-full">
      <div className="flex flex-col w-2/3 pr-5 border-r-2 border-gray-200">
        <div>
          <h2 className="mb-3 text-4xl font-semibold opacity-90">Settings</h2>
        </div>
        <div className="flex flex-col gap-1">
          <div className="flex flex-row justify-between items-center opacity-80">
            <p className="mb-3 text-3xl">Walls</p>
            <div className="flex flex-row items-center  gap-3">
              <p className="font-bold text-3xl">{wallState}</p>
              <div className="flex flex-col text-2xl">
                <button onClick={addWall}>+</button>
                <button onClick={subWall}>-</button>
              </div>
            </div>
          </div>
          <div className="flex flex-row justify-between items-center opacity-80">
            <p className="mb-3 text-3xl">Coats</p>
            <div className="flex flex-row items-center  gap-3">
              <p className="font-bold text-3xl">{coatState}</p>
              <div className="flex flex-col text-2xl">
                <button onClick={addCoat}>+</button>
                <button onClick={subCoat}>-</button>
              </div>
            </div>
          </div>
          <div className="flex flex-row justify-between items-center opacity-80">
            <p className="mb-3 text-3xl">Brands</p>
            <Select
              size="md"
              items={brands}
              label="Paint Brands"
              placeholder="Select a paint brand"
              selectedKeys={brand}
              className="max-w-xs"
              onSelectionChange={setBrand}
            >
              {(brands) => (
                <SelectItem key={brands.value}>{brands.label}</SelectItem>
              )}
            </Select>
          </div>
          <Accordion selectionMode="multiple" disabledKeys={disabled_keys}>
            <AccordionItem
              key="1"
              aria-label="Wall 1"
              title={<p className="text-3xl opacity-80">Wall 1</p>}
            >
              <AccordionWall></AccordionWall>
            </AccordionItem>
            <AccordionItem
              key="2"
              aria-label="Wall 2"
              title={<p className="text-3xl opacity-80">Wall 2</p>}
            >
              <AccordionWall></AccordionWall>
            </AccordionItem>
          </Accordion>
        </div>
      </div>
      <div className="flex flex-col w-1/3">
        <div className="sticky top-5 pl-16">
          <div className="flex flex-col justify-between">
            <h2 className="mb-3 text-4xl font-semibold opacity-90">Total</h2>
            <Button onClick={(e) => callAPI(wallState)}>Get Total</Button>
            {/* <Button onClick={handleAPI}>Get Total</Button> */}
            <p>{data}</p>
          </div>
        </div>
      </div>
    </main>
  );
}
