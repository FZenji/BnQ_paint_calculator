"use client";

import { useState, useMemo } from "react";
import { Accordion, AccordionItem } from "@nextui-org/accordion";
import { Input } from "@nextui-org/input";
import { Checkbox } from "@nextui-org/checkbox";

export default function AccordianWall() {
  const [measureW, setMeasureW] = useState("0");
  const [measureH, setMeasureH] = useState("0");
  const [areObsticles1, setAreObsticles1] = useState(false);

  const validateMeasurement = (measure) =>
    measure.match("^(?:[1-9]|[1-4]\\d|50)$");

  const isInvalidW = useMemo(() => {
    if (measureW === "") return false;

    return validateMeasurement(measureW) ? false : true;
  }, [measureW]);

  const isInvalidH = useMemo(() => {
    if (measureH === "") return false;

    return validateMeasurement(measureH) ? false : true;
  }, [measureH]);
  return (
    <div className="flex flex-col gap-2">
      <Input
        type="width1"
        label="Width"
        isInvalid={isInvalidW}
        color={isInvalidW ? "danger" : "default"}
        onValueChange={setMeasureW}
      />
      <Input
        type="height1"
        label="Height"
        isInvalid={isInvalidH}
        color={isInvalidH ? "danger" : "default"}
        onValueChange={setMeasureH}
      />
    </div>
  );
}
