import {
  AlertDialog,
  AlertDialogBody,
  AlertDialogContent,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogOverlay,
  Button,
} from "@chakra-ui/react"
import { useQuery } from "@tanstack/react-query"
import React from "react"

import {PollsService} from "../../client"
import useCustomToast from "../../hooks/useCustomToast"

interface PredictPollProps {
  isOpen: boolean
  onClose: () => void
}

const PredictPolls = ({isOpen, onClose }: PredictPollProps) => {
  const showToast = useCustomToast()
  const cancelRef = React.useRef<HTMLButtonElement | null>(null)
  const {
    data: predict,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ["predict"],
    queryFn: () => PollsService.predictPolls({})
  });

  if (isError) {
    const errDetail = (error as any).body?.detail
    showToast("Something went wrong.", `${errDetail}`, "error")
  }

  return (
    <AlertDialog
      isOpen={isOpen}
      leastDestructiveRef={cancelRef}
      onClose={onClose}
      isCentered
    >
      <AlertDialogOverlay>
        <AlertDialogContent>
          <AlertDialogHeader>Prediction</AlertDialogHeader>
          <AlertDialogBody>
            {isLoading && <div>Loading...</div>}
            {isError && <div>Error: {error.message}</div>}
            {predict && (
              <div>
                <p>{predict.message}</p>
              </div>
            )}
          </AlertDialogBody>
          <AlertDialogFooter gap={3}>
            <Button ref={cancelRef} onClick={onClose}>
              Cancel
            </Button>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialogOverlay>
    </AlertDialog>
  );
};
export default PredictPolls;
